// Common interfaces and types
export interface TwitchMessage {
  id: string;
  username: string;
  message: string;
  timestamp: string;
  badges?: string[];
  color?: string;
}

export interface TwitchUser {
  id: string;
  username: string;
  displayName: string;
  profileImage?: string;
}

export interface ApiResponse<T> {
  data: T;
  error?: string;
  status: number;
} 