import { LoginLink, RegisterLink } from "@kinde-oss/kinde-auth-nextjs/components"

import { Button } from "@/components/ui/button"

export default function LoginPage() {
    return (
        <main className = "h-dvh flex flex-col items-center gap-6 text-4xl p-4">
            <h1>SMIP Sign In</h1>
            <Button asChild>
                <LoginLink>Login</LoginLink>
            </Button>
            <Button asChild>
                <RegisterLink>Register</RegisterLink>
            </Button>
        </main>
    )
}