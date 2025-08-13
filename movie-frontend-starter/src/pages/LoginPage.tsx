import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { TextField, Button, Stack, Alert, Paper, Typography } from '@mui/material'
import { useLogin } from '../api/auth'
import { useAuthStore } from '../state/auth'
import { z } from 'zod'
import { useLocation, useNavigate } from 'react-router-dom'

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(6)
})
type FormValues = z.infer<typeof schema>

export default function LoginPage() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormValues>({ resolver: zodResolver(schema) })
  const login = useLogin()
  const navigate = useNavigate()
  const location = useLocation() as any
  const from = location.state?.from?.pathname || '/'
  const { login: saveAuth } = useAuthStore()

  const onSubmit = (values: FormValues) => {
    login.mutate(values, {
      onSuccess: (data) => {
        saveAuth({ user: {
          id: data.id, name: data.name, last_name: data.last_name, email: data.email, phone_number: data.phone_number
        }, token: data.token })
        navigate(from, { replace: true })
      }
    })
  }

  return (
    <Paper sx={{ p: 3, maxWidth: 420, mx: 'auto' }}>
      <Typography variant="h6" gutterBottom>Login</Typography>
      <form onSubmit={handleSubmit(onSubmit)}>
        <Stack spacing={2}>
          <TextField label="Email" {...register('email')} error={!!errors.email} helperText={errors.email?.message} />
          <TextField label="Password" type="password" {...register('password')} error={!!errors.password} helperText={errors.password?.message} />
          {login.isError && <Alert severity="error">{(login.error as any)?.response?.data?.detail || 'Login failed'}</Alert>}
          <Button type="submit" variant="contained" disabled={login.isPending}>Login</Button>
        </Stack>
      </form>
    </Paper>
  )
}
