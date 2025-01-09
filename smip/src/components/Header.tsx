import { HomeIcon, CalculatorIcon, UsersRound, ChartLineIcon, LogOut } from 'lucide-react';
import { NavButton } from "@/components/NavButton"
import Link from 'next/link';
import { ModeToggle } from '@/components/ModeToggle';
import { LogoutLink } from '@kinde-oss/kinde-auth-nextjs/components';
import { Button } from '@/components/ui/button';
export function Header(){
    return (
        <header className="bg-background h-12 p-2 border-b sticky top-0 z-20">
            <div className="flex h-8 items-center justify-between w-full">
                <div className="flex items-center gap-2">
                    <NavButton href="/home" label="My Home" icon={HomeIcon} />
                    <Link href="/home" className="flex justify-center items-center gap-2 ml-0" title="Home">
                        <h1 className="hidden sm:block text-l font-serif font-bold m-0 mt-1">
                            SMIP
                        </h1>
                    </Link>
                </div>

                <div className="flex items-center">
                    <NavButton href="/mytrades" label="MyTrades" icon={ChartLineIcon} />
                    <NavButton href="/social" label="Social" icon={UsersRound} />
                    <NavButton href="/calculator" label="Calculator" icon={CalculatorIcon} />
                    <ModeToggle/>

                    <Button
                    variant='ghost'
                    size='icon'
                    aria-label='LogOut'
                    title='LogOut'
                    className='rounded-full'
                    asChild
                    >
                        <LogoutLink>
                            <LogOut />
                        </LogoutLink>
                    </Button>
                </div>

            </div>
        </header>
    )
}