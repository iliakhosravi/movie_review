  import axios from 'axios'
  import { useAuthStore } from '../state/auth'

  export const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL, // http://localhost:8000/api/user
  })

  api.interceptors.request.use((config) => {
    const token = useAuthStore.getState().token
    if (token) {
      config.headers = config.headers ?? {}
      ;(config.headers as any).Authorization = `Bearer ${token}`
    }
    if (import.meta.env.DEV) {
      console.log('[REQ]', (config.method||'get').toUpperCase(), (config.baseURL||'')+(config.url||''), 'Auth?', !!(config.headers as any).Authorization)
    }
    return config
  })

  api.interceptors.response.use(
    (res) => res,
    (err) => {
      if (import.meta.env.DEV) {
        const cfg = err.config || {}
        console.error('[ERR]', err.response?.status, `${cfg.baseURL||''}${cfg.url||''}`, err.response?.data || err.message)
      }
      return Promise.reject(err)
    }
  )
