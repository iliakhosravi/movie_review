import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { TextField, Button, Stack, Alert, Paper, Typography } from '@mui/material'
import { useSignup } from '../api/auth'
import { z } from 'zod'
import { useNavigate } from 'react-router-dom'

const schema = z.object({
  name: z.string().min(1),
  last_name: z.string().min(1),
  phone_number: z.string().min(7),
  email: z.string().email(),
  password: z.string().min(6)
})
type FormValues = z.infer<typeof schema>

export default function SignupPage() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormValues>({ resolver: zodResolver(schema) })
  const signup = useSignup()
  const navigate = useNavigate()

  const onSubmit = (values: FormValues) => {
    signup.mutate(values, {
      onSuccess: () => navigate('/login')
    })
  }

  return (
    <Paper sx={{ p: 3, maxWidth: 520, mx: 'auto' }}>
      <Typography variant="h6" gutterBottom>Sign up</Typography>
      <form onSubmit={handleSubmit(onSubmit)}>
        <Stack spacing={2}>
          <TextField label="Name" {...register('name')} error={!!errors.name} helperText={errors.name?.message} />
          <TextField label="Last name" {...register('last_name')} error={!!errors.last_name} helperText={errors.last_name?.message} />
          <TextField label="Phone number" {...register('phone_number')} error={!!errors.phone_number} helperText={errors.phone_number?.message} />
          <TextField label="Email" {...register('email')} error={!!errors.email} helperText={errors.email?.message} />
          <TextField label="Password" type="password" {...register('password')} error={!!errors.password} helperText={errors.password?.message} />
          {signup.isError && <Alert severity="error">Sign up failed</Alert>}
          <Button type="submit" variant="contained" disabled={signup.isPending}>Create account</Button>
        </Stack>
      </form>
    </Paper>
  )
}
