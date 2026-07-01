export interface Application {
  id: string;
  title: string;
  description: string | null;
  status: 'new' | 'in_progress' | 'done';
  priority: 'low' | 'normal' | 'high';
  created_at: string;
  updated_at: string;
}

export interface ListParams {
  offset: number;
  limit: number;
  query?: string;
  statuses?: string[];
  priorities?: string[];
  sort_by_priority?: boolean;
  sort_desc?: boolean;       
}
