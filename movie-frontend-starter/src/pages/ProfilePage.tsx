import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { TextField, Button, Stack, Alert, Paper, Typography } from '@mui/material'
import { useAuthStore } from '../state/auth'
import { api } from '../api/client'
import { z } from 'zod'

const schema = z.object({
  name: z.string().min(1, 'Required'),
  last_name: z.string().min(1, 'Required'),
  phone_number: z.string().min(7, 'At least 7 chars'),
})
type FormValues = z.infer<typeof schema>

function renderError(err: unknown) {
  const data = (err as any)?.response?.data
  if (!data) return 'Update failed'
  if (typeof data === 'string') return data
  try {
    return Object.entries(data)
      .map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(', ') : String(v)}`)
      .join(' | ')
  } catch {
    return 'Update failed'
  }
}

export default function ProfilePage() {
  const { user, updateUser } = useAuthStore()
  const [banner, setBanner] = useState<{ type: 'success' | 'error' | null; text?: string }>({ type: null })
  const [submitting, setSubmitting] = useState(false)

  if (!user) {
    return <Alert severity="warning">Please login first.</Alert>
  }

  const { register, handleSubmit, formState: { errors } } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: { name: user.name, last_name: user.last_name, phone_number: user.phone_number },
  })

  const onSubmit = handleSubmit(async (values) => {
    setBanner({ type: null })
    setSubmitting(true)
    try {
      const res = await api.patch('/me/', values) // trailing slash مهم
      const data = res.data as { name: string; last_name: string; phone_number: string }
      // به‌روزرسانی استور یا fallback
      try {
        if (typeof updateUser === 'function') {
          updateUser({ name: data.name, last_name: data.last_name, phone_number: data.phone_number })
        } else {
          // fallback: اگر به هر دلیلی updateUser نبود
          const updated = { ...user, ...data }
          localStorage.setItem('user', JSON.stringify(updated))
        }
      } catch {
        const updated = { ...user, ...data }
        localStorage.setItem('user', JSON.stringify(updated))
      }
      setBanner({ type: 'success', text: 'Profile updated.' })
    } catch (err) {
      console.error('PATCH /me error:', err)
      setBanner({ type: 'error', text: renderError(err) })
    } finally {
      setSubmitting(false)
    }
  })

  return (
    <Paper sx={{ p: 3, maxWidth: 520, mx: 'auto' }}>
      <Typography variant="h6" gutterBottom>My Profile</Typography>
      <Typography variant="body2" gutterBottom>Email: {user.email}</Typography>

      <form onSubmit={onSubmit}>
        <Stack spacing={2}>
          <TextField label="Name" {...register('name')} error={!!errors.name} helperText={errors.name?.message} />
          <TextField label="Last name" {...register('last_name')} error={!!errors.last_name} helperText={errors.last_name?.message} />
          <TextField label="Phone number" {...register('phone_number')} error={!!errors.phone_number} helperText={errors.phone_number?.message} />

          {banner.type === 'error' && <Alert severity="error">{banner.text}</Alert>}
          {banner.type === 'success' && <Alert severity="success">{banner.text}</Alert>}

          <Button type="submit" variant="contained" disabled={submitting}>
            {submitting ? 'Saving…' : 'Save'}
          </Button>
        </Stack>
      </form>
    </Paper>
  )
}
