//import Image from "next/image";
import Link from "next/link"
import Image from "next/image"

export default function Home() {
  return (
    <div className="bg-white">

      <main className="flex flex-col justify-center text-center max-w-5xl mx-auto h-dvh">

        <div className="flex flex-col gap-6 p-12 rounded-xl bg-black/90 w-4/5 sm:max-w-96 mx-auto text-white sm:text-2xl">
          <h1>Welcome to SMIP</h1> 
          <h1>A stock market inspired game to invest in your favorite social media posts</h1>
          <div className="w-1/4 mx-auto">
            <Link href="https://github.com/rithkott/SMIP">
              <Image 
                src="/images/github-mark-white.svg" 
                alt="Link to Github"
                layout="responsive" 
                className="rounded-lg mx-auto"
                width={100}
                height={100}
                />
            </Link>
          </div>
        </div>

      </main>

    </div>
  );
}
