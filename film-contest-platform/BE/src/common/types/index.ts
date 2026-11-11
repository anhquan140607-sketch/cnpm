import { Request } from 'express';

export type UserRole = 'administrator' | 'organizer' | 'judge' | 'participant';
export type UserStatus = 'active' | 'inactive' | 'suspended';

export type ContestStatus = 'draft' | 'open' | 'closed' | 'judging' | 'published' | 'archived';
export type SubmissionStatus = 
  | 'submitted' 
  | 'under_verification' 
  | 'accepted' 
  | 'rejected' 
  | 'needs_revision' 
  | 'withdrawn';

export interface JwtPayload {
  id: number;
  email: string;
  role: UserRole;
  name: string;
}

export interface RequestWithUser extends Request {
  user?: JwtPayload;
}

export interface ApiResponse<T = any> {
  success: boolean;
  message?: string;
  data?: T;
  error?: {
    code?: string;
    message: string;
    details?: any;
  };
  meta?: {
    page?: number;
    limit?: number;
    total?: number;
    [key: string]: any;
  };
}
