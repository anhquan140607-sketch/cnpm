import { UserRole } from '../../common/types/index.js';

export interface RegisterDto {
  name: string;
  email: string;
  password: string;
  phone?: string;
  bio?: string;
}

export interface LoginDto {
  email: string;
  password: string;
}

export interface RefreshTokenDto {
  refreshToken: string;
}

export interface ChangePasswordDto {
  oldPassword: string;
  newPassword: string;
}

export interface UpdateProfileDto {
  name?: string;
  phone?: string;
  bio?: string;
  avatar_url?: string;
}

export interface CreateUserDto {
  name: string;
  email: string;
  password: string;
  role: UserRole;
  phone?: string;
  bio?: string;
}
