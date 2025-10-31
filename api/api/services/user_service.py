"""
User service for authentication and user management
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
from api.models.user import User, Role, Permission, UserSession, EmailVerification, PasswordReset
from api.core.jwt_auth import JWTAuth, create_token_pair
from api.schemas.user import UserCreate, UserUpdate, UserLogin, UserResponse
import structlog
import secrets
import uuid

logger = structlog.get_logger()


class UserService:
    """Service for user authentication and management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_user(self, user_data: UserCreate) -> User:
        """Create a new user"""
        try:
            # Check if user already exists
            existing_user = await self.get_user_by_email(user_data.email)
            if existing_user:
                raise ValueError("User with this email already exists")
            
            # Hash password
            password_hash = JWTAuth.get_password_hash(user_data.password)
            
            # Create user
            user = User(
                email=user_data.email,
                password_hash=password_hash,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                company=user_data.company,
                phone=user_data.phone,
                country_code=user_data.country_code,
                is_verified=True  # Auto-verify for presentation purposes
            )
            
            self.db.add(user)
            await self.db.flush()  # Flush to get user.id WITHOUT committing
            # CRITICAL: Store user.id immediately after flush, BEFORE commit
            # After commit, accessing user.id can trigger expiration reload causing greenlet errors
            user_id_str = str(user.id)
            await self.db.commit()
            
            # Assign role based on user type
            # Use stored user_id_str (never access user.id after commit)
            role_assigned = False
            if user_data.user_type == "developer":
                role_assigned = await self.assign_role_to_user(user_id_str, "developer")
                logger.info("Developer role assignment", user_id=user_id_str, success=role_assigned)
            else:
                role_assigned = await self.assign_role_to_user(user_id_str, "viewer")
                logger.info("Viewer role assignment", user_id=user_id_str, success=role_assigned)
            
            if not role_assigned:
                logger.warning("Role assignment failed or role already assigned", user_id=user_id_str, user_type=user_data.user_type)
                raise ValueError(f"Failed to assign {user_data.user_type} role to user")
            
            # Ensure role assignment is committed
            await self.db.commit()
            
            # Expire any cached user objects to force fresh reload
            # This ensures we get the newly assigned role
            if user in self.db:
                self.db.expire(user)
            
            # Reload user with roles and permissions loaded (fresh query in same session)
            # Use selectinload to eagerly load everything before returning
            from sqlalchemy.orm import selectinload
            result = await self.db.execute(
                select(User)
                .options(
                    selectinload(User.roles).selectinload(Role.permissions)
                )
                .where(User.id == user_id_str)
            )
            user_with_roles = result.scalar_one_or_none()
            
            if not user_with_roles:
                raise ValueError("Failed to reload user after role assignment")
            
            # Verify and access all relationships WHILE still in async context
            # Force access to roles immediately after query
            roles_collection = user_with_roles.roles
            roles_list = list(roles_collection) if roles_collection else []
            
            if not roles_list:
                # Double-check by querying junction table directly
                from api.models.user import user_roles
                check_roles = await self.db.execute(
                    select(user_roles.c.role_id).where(user_roles.c.user_id == user_id_str)
                )
                role_ids = [r[0] for r in check_roles.fetchall()]
                
                if role_ids:
                    # Roles exist in DB but not loaded - force reload
                    logger.warning("Roles exist but not loaded, forcing reload", user_id=user_id_str, role_ids=role_ids)
                    # Try one more time with explicit refresh
                    await self.db.refresh(user_with_roles, ["roles"])
                    roles_list = list(user_with_roles.roles) if user_with_roles.roles else []
                
                if not roles_list:
                    logger.error("User has no roles after assignment", user_id=user_id_str, user_type=user_data.user_type, role_ids_in_db=role_ids)
                    raise ValueError(f"Failed to assign {user_data.user_type} role to user")
            
            # Force access to all permissions for each role (while session is active)
            role_names = []
            for role in roles_list:
                role_names.append(role.name)
                permissions_list = list(role.permissions) if role.permissions else []
                # Store permission names on role object for later access
                role._permission_names = [p.name for p in permissions_list]
            
            logger.info("User roles loaded", user_id=user_id_str, roles=role_names)
            
            # Use the reloaded user (relationships are now eagerly loaded)
            user = user_with_roles
            
            # Create email verification token (use email from user_data to avoid relationship access)
            await self.create_email_verification(user_id_str, user_data.email)
            
            logger.info("User created successfully", user_id=user_id_str, email=user_data.email)
            return user
            
        except Exception as e:
            await self.db.rollback()
            logger.error("Failed to create user", error=str(e), email=user_data.email)
            raise
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID with roles and permissions"""
        try:
            # Eagerly load roles and their permissions
            result = await self.db.execute(
                select(User)
                .options(
                    selectinload(User.roles).selectinload(Role.permissions)
                )
                .where(User.id == user_id)
            )
            user = result.scalar_one_or_none()
            
            if user:
                # Force access to relationships to ensure they're loaded
                # This ensures lazy relationships are fetched before session closes
                _ = user.roles  # Access roles
                for role in user.roles:
                    _ = role.permissions  # Access permissions for each role
            
            return user
        except Exception as e:
            logger.error("Failed to get user by ID", error=str(e), user_id=user_id, exc_info=True)
            return None
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email with roles and permissions"""
        try:
            # Eagerly load roles and their permissions
            result = await self.db.execute(
                select(User)
                .options(
                    selectinload(User.roles).selectinload(Role.permissions)
                )
                .where(User.email == email)
            )
            user = result.scalar_one_or_none()
            
            if user:
                # Force access to relationships to ensure they're loaded
                _ = user.roles  # Access roles
                for role in user.roles:
                    _ = role.permissions  # Access permissions for each role
            
            return user
        except Exception as e:
            logger.error("Failed to get user by email", error=str(e), email=email, exc_info=True)
            return None
    
    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        try:
            user = await self.get_user_by_email(email)
            if not user:
                return None
            
            # Check if user is locked
            if user.locked_until and user.locked_until > datetime.utcnow():
                logger.warning("Login attempt on locked account", email=email)
                return None
            
            # Verify password
            if not JWTAuth.verify_password(password, user.password_hash):
                # Increment failed login attempts
                user.failed_login_attempts += 1
                
                # Lock account after 5 failed attempts
                if user.failed_login_attempts >= 5:
                    user.locked_until = datetime.utcnow() + timedelta(minutes=30)
                    logger.warning("Account locked due to failed login attempts", email=email)
                
                await self.db.commit()
                return None
            
            # Reset failed login attempts on successful login
            user.failed_login_attempts = 0
            user.locked_until = None
            user.last_login = datetime.utcnow()
            
            await self.db.commit()
            
            logger.info("User authenticated successfully", user_id=user.id, email=email)
            return user
            
        except Exception as e:
            logger.error("Authentication failed", error=str(e), email=email)
            return None
    
    async def update_user(self, user_id: str, user_data: UserUpdate) -> Optional[User]:
        """Update user information"""
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                return None
            
            # Update fields
            if user_data.first_name is not None:
                user.first_name = user_data.first_name
            if user_data.last_name is not None:
                user.last_name = user_data.last_name
            if user_data.company is not None:
                user.company = user_data.company
            if user_data.phone is not None:
                user.phone = user_data.phone
            if user_data.country_code is not None:
                user.country_code = user_data.country_code
            
            user.updated_at = datetime.utcnow()
            
            await self.db.commit()
            await self.db.refresh(user)
            
            logger.info("User updated successfully", user_id=user_id)
            return user
            
        except Exception as e:
            await self.db.rollback()
            logger.error("Failed to update user", error=str(e), user_id=user_id)
            return None
    
    async def change_password(self, user_id: str, old_password: str, new_password: str) -> bool:
        """Change user password"""
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                return False
            
            # Verify old password
            if not JWTAuth.verify_password(old_password, user.password_hash):
                return False
            
            # Hash new password
            user.password_hash = JWTAuth.get_password_hash(new_password)
            user.password_changed_at = datetime.utcnow()
            
            await self.db.commit()
            
            logger.info("Password changed successfully", user_id=user_id)
            return True
            
        except Exception as e:
            await self.db.rollback()
            logger.error("Failed to change password", error=str(e), user_id=user_id)
            return False
    
    async def assign_role_to_user(self, user_id: str, role_name: str) -> bool:
        """Assign a role to a user"""
        try:
            # Get role first
            role = await self.get_role_by_name(role_name)
            if not role:
                logger.error("Role not found", role_name=role_name)
                return False
            
            # Check if user already has this role by querying junction table directly
            from api.models.user import user_roles
            check_result = await self.db.execute(
                select(user_roles).where(
                    user_roles.c.user_id == user_id,
                    user_roles.c.role_id == role.id
                )
            )
            if check_result.first():
                logger.info("User already has role", user_id=user_id, role_name=role_name)
                return True
            
            # Insert directly into junction table to avoid relationship lazy loading issues
            # This avoids the greenlet error when accessing user.roles.append(role)
            from sqlalchemy import insert
            # Store role.id before any relationship access
            role_id_str = str(role.id)
            insert_stmt = insert(user_roles).values(
                user_id=user_id,
                role_id=role_id_str
            )
            await self.db.execute(insert_stmt)
            # Commit in separate transaction to ensure it's persisted
            await self.db.commit()
            # Flush to ensure it's visible immediately
            await self.db.flush()
            
            logger.info("Role assigned to user successfully", user_id=user_id, role_name=role_name, role_id=role_id_str)
            return True
            
        except Exception as e:
            await self.db.rollback()
            logger.error("Failed to assign role", error=str(e), user_id=user_id, role_name=role_name, exc_info=True)
            return False
    
    async def remove_role_from_user(self, user_id: str, role_name: str) -> bool:
        """Remove a role from a user"""
        try:
            user = await self.get_user_by_id(user_id)
            role = await self.get_role_by_name(role_name)
            
            if not user or not role:
                return False
            
            # Remove role from user
            if role in user.roles:
                user.roles.remove(role)
                await self.db.commit()
            
            logger.info("Role removed from user", user_id=user_id, role_name=role_name)
            return True
            
        except Exception as e:
            await self.db.rollback()
            logger.error("Failed to remove role", error=str(e), user_id=user_id, role_name=role_name)
            return False
    
    async def get_role_by_name(self, role_name: str) -> Optional[Role]:
        """Get role by name"""
        try:
            result = await self.db.execute(
                select(Role)
                .options(selectinload(Role.permissions))
                .where(Role.name == role_name)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error("Failed to get role by name", error=str(e), role_name=role_name)
            return None
    
    async def create_email_verification(self, user_id: str, email: str) -> str:
        """Create email verification token"""
        try:
            token = secrets.token_urlsafe(32)
            expires_at = datetime.utcnow() + timedelta(hours=24)
            
            verification = EmailVerification(
                user_id=user_id,
                token=token,
                email=email,
                expires_at=expires_at
            )
            
            self.db.add(verification)
            await self.db.commit()
            
            logger.info("Email verification token created", user_id=user_id)
            return token
            
        except Exception as e:
            await self.db.rollback()
            logger.error("Failed to create email verification", error=str(e), user_id=user_id)
            raise
    
    async def verify_email(self, token: str) -> bool:
        """Verify email with token"""
        try:
            result = await self.db.execute(
                select(EmailVerification)
                .where(
                    and_(
                        EmailVerification.token == token,
                        EmailVerification.is_used == False,
                        EmailVerification.expires_at > datetime.utcnow()
                    )
                )
            )
            verification = result.scalar_one_or_none()
            
            if not verification:
                return False
            
            # Mark verification as used
            verification.is_used = True
            
            # Update user as verified
            user = await self.get_user_by_id(verification.user_id)
            if user:
                user.is_verified = True
                user.email_verified_at = datetime.utcnow()
            
            await self.db.commit()
            
            logger.info("Email verified successfully", user_id=verification.user_id)
            return True
            
        except Exception as e:
            await self.db.rollback()
            logger.error("Failed to verify email", error=str(e), token=token)
            return False
    
    async def create_password_reset(self, email: str) -> Optional[str]:
        """Create password reset token"""
        try:
            user = await self.get_user_by_email(email)
            if not user:
                return None
            
            token = secrets.token_urlsafe(32)
            expires_at = datetime.utcnow() + timedelta(hours=1)
            
            reset = PasswordReset(
                user_id=user.id,
                token=token,
                expires_at=expires_at
            )
            
            self.db.add(reset)
            await self.db.commit()
            
            logger.info("Password reset token created", user_id=user.id)
            return token
            
        except Exception as e:
            await self.db.rollback()
            logger.error("Failed to create password reset", error=str(e), email=email)
            return None
    
    async def reset_password(self, token: str, new_password: str) -> bool:
        """Reset password with token"""
        try:
            result = await self.db.execute(
                select(PasswordReset)
                .where(
                    and_(
                        PasswordReset.token == token,
                        PasswordReset.is_used == False,
                        PasswordReset.expires_at > datetime.utcnow()
                    )
                )
            )
            reset = result.scalar_one_or_none()
            
            if not reset:
                return False
            
            # Mark reset as used
            reset.is_used = True
            
            # Update user password
            user = await self.get_user_by_id(reset.user_id)
            if user:
                user.password_hash = JWTAuth.get_password_hash(new_password)
                user.password_changed_at = datetime.utcnow()
                user.failed_login_attempts = 0
                user.locked_until = None
            
            await self.db.commit()
            
            logger.info("Password reset successfully", user_id=reset.user_id)
            return True
            
        except Exception as e:
            await self.db.rollback()
            logger.error("Failed to reset password", error=str(e), token=token)
            return False
    
    async def create_user_session(self, user: User, ip_address: str = None, user_agent: str = None, role_names: list = None) -> Dict[str, str]:
        """Create user session with tokens"""
        try:
            # Create token pair with role names (if provided, avoids lazy loading)
            tokens = create_token_pair(user, role_names=role_names)
            
            # Create session record
            session = UserSession(
                user_id=user.id,
                session_token=tokens["access_token"],
                refresh_token=tokens["refresh_token"],
                ip_address=ip_address,
                user_agent=user_agent,
                expires_at=datetime.utcnow() + timedelta(days=7)
            )
            
            self.db.add(session)
            await self.db.commit()
            
            logger.info("User session created", user_id=user.id)
            return tokens
            
        except Exception as e:
            await self.db.rollback()
            logger.error("Failed to create user session", error=str(e), user_id=user.id)
            raise
    
    async def refresh_user_session(self, refresh_token: str) -> Optional[Dict[str, str]]:
        """Refresh user session with refresh token"""
        try:
            # Find session
            result = await self.db.execute(
                select(UserSession)
                .options(selectinload(UserSession.user).selectinload(User.roles).selectinload(Role.permissions))
                .where(
                    and_(
                        UserSession.refresh_token == refresh_token,
                        UserSession.is_active == True,
                        UserSession.expires_at > datetime.utcnow()
                    )
                )
            )
            session = result.scalar_one_or_none()
            
            if not session:
                return None
            
            # Create new token pair
            tokens = create_token_pair(session.user)
            
            # Update session
            session.session_token = tokens["access_token"]
            session.refresh_token = tokens["refresh_token"]
            session.last_activity = datetime.utcnow()
            
            await self.db.commit()
            
            logger.info("User session refreshed", user_id=session.user_id)
            return tokens
            
        except Exception as e:
            await self.db.rollback()
            logger.error("Failed to refresh user session", error=str(e))
            return None
    
    async def revoke_user_session(self, refresh_token: str) -> bool:
        """Revoke user session"""
        try:
            result = await self.db.execute(
                select(UserSession)
                .where(UserSession.refresh_token == refresh_token)
            )
            session = result.scalar_one_or_none()
            
            if session:
                session.is_active = False
                await self.db.commit()
            
            logger.info("User session revoked", user_id=session.user_id if session else None)
            return True
            
        except Exception as e:
            await self.db.rollback()
            logger.error("Failed to revoke user session", error=str(e))
            return False
