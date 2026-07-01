import { apiClient } from './client';
import { Application, ListParams } from '../types/application';

export const applicationApi = {
  create: (data: { title: string; description?: string; status: string; priority: string }) => 
    apiClient.post('/applications/', data),
  getAll: (params: ListParams) => {
    const searchParams = new URLSearchParams();
    if (params.query) searchParams.append('query', params.query);
    searchParams.append('offset', String(params.offset));
    searchParams.append('limit', String(params.limit));
    searchParams.append('sort_desc', String(params.sort_desc));
    searchParams.append('sort_by_priority', String(params.sort_by_priority));
    params.statuses?.forEach(status => searchParams.append('statuses', status));
    params.priorities?.forEach(priority => searchParams.append('priorities', priority));
    return apiClient.get<Application[]>('/applications/', { params: searchParams });
  },
  update: (id: string, data: any) => 
    apiClient.patch(`/applications/${id}`, data),

  deleteMany: (ids: string[]) => 
    apiClient.delete('/applications/delete-many', { data: ids }),
};