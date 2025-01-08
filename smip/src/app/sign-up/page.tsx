"use client"
 
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"
 
import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import {useCreateUserWithEmailAndPassword} from 'react-firebase-hooks/auth'
import { auth } from '@/app/firebase/config'

const formSchema = z.object({
  email: z.string()
    .email({message: "Please enter a valid email address"})
    .nonempty({message: "Email is required"}),
  username: z.string().min(3, {
    message: "Username must be at least 3 characters.",
  }),
  password: z
    .string()
    .min(6, {message: "Password must be at least 6 characters.",})
    .regex(/^[^'";\\]+$/, {message: "Password cannot contain dangerous characters like ' \" ; \\",})
})
 
export default function ProfileForm() {
    const form = useForm({
        resolver: zodResolver(formSchema),
        defaultValues: {
            email: "",
            username: "",
            password: "",
        },
      })

    const [createUserWithEmailAndPassword] = useCreateUserWithEmailAndPassword(auth)
    const OnSubmit = async (data: z.infer<typeof formSchema>) => {

        try{
          const res = await createUserWithEmailAndPassword(data["email"], data["password"])
          console.log({res})
          sessionStorage.setItem('user', 'true')

        } catch(e){
          console.error(e)
        }
      }
      

    return (
      <div className="flex flex-col justify-center text-left w-1/2 mx-auto h-dvh">
        <Form {...form}>
        <form onSubmit={form.handleSubmit(OnSubmit)} className="space-y-8">
        <FormField
            control={form.control}
            name="email"
            render={({ field }) => (
                <FormItem>
                    <FormLabel>Email</FormLabel>
                        <FormControl>
                            <Input placeholder="email" {...field} />
                        </FormControl>
                    <FormMessage />
                </FormItem>
            )}
            />
            <FormField
            control={form.control}
            name="username"
            render={({ field }) => (
                <FormItem>
                    <FormLabel>Username</FormLabel>
                        <FormControl>
                            <Input placeholder="username" {...field} />
                        </FormControl>
                        <FormDescription>
                            This is your public display name.
                        </FormDescription>
                    <FormMessage />
                </FormItem>
            )}
            />
            <FormField
            control={form.control}
            name="password"
            render={({ field }) => (
                <FormItem>
                    <FormLabel>Password</FormLabel>
                    <FormControl>
                        <Input placeholder="password" {...field} />
                    </FormControl>
                    <FormMessage />
                </FormItem>
            )}
            />
            <Button type="submit">Submit</Button>
        </form>
        </Form>
      </div>
    )
}