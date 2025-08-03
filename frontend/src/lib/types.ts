export interface User {
  id: number;
  email: string;
  name: string;
  created_at: string;
}

export interface FeatureBase {
  title: string;
  description: string;
  category: "BUG" | "FEATURE" | "ENHANCEMENT";
}

export type FeatureCreate = FeatureBase;

export interface FeatureResponse extends FeatureBase {
  id: number;
  status: "Open" | "Closed";
  created_at: string;
  user_id: number;
  like_count: number;
}

export interface Vote {
  id: number;
  feature_id: number;
  user_id: number;
  created_at: string;
}

export interface APIError {
  response?: {
    data?: {
      error?: string;
      message?: string;
    };
    status?: number;
  };
}
