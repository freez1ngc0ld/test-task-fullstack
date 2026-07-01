import { apiClient } from './client';

export const adminApi = {
  signin: (username: string, password: string) => {
    const body = new URLSearchParams({ username, password });
    return apiClient.post('/admin/signin', body, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
  },
  signup: (username: string, password: string) => 
    apiClient.post('/admin/signup', { username, password }),
  changePassword: (old_password: string, new_password: string) => 
    apiClient.patch('/admin/change-password', { old_password, new_password }),
  deleteAccount: (admin_2_delete_id: string, password?: string) => 
    apiClient.delete('/admin/delete-account', { data: { admin_2_delete_id, password } }),

  deleteMyAccount: (password: string) => 
    apiClient.delete('/admin/delete-account/me', { data: { password } }),
  listAdmins: (offset: number, limit: number) => 
    apiClient.get('/admin/all', { params: { offset, limit } }),
  getMe: () => apiClient.get('/admin/me'),
};