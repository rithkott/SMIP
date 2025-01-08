import Link from 'next/link'
import Image from 'next/image'
export const metadata = {
    title: "Page not found"
}
 
export default function NotFound() {
  return (
    <div>
        <div className="flex flex-col justify-center text-center max-w-5xl mx-auto h-dvh">
            <div className="mb-6">
                <h1 className="font-serif font-bold">Not Found</h1>
                <Link href="/">Return Home</Link>
            </div>
            <div className="flex flex-col justify-center items-center">
                <Image 
                    src="/images/404notfound.svg" 
                    alt="Page not found"
                    layout="intrinsic" 
                    className="m-0 rounded-xl"
                    width={300}
                    height={300}
                    sizes="300px"
                />
            </div>
        </div>
    </div>
    
    
  )
}