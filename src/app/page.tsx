"use client"

//import Image from "next/image";
import Link from "next/link"
import Image from "next/image"
import { Button } from "@/components/ui/button";
import { BackgroundBeams } from "@/components/ui/background-beams";

export default function Home() {

  return (
    <div className="relative">

      <main className="flex flex-col justify-center text-center max-w-5xl mx-auto h-dvh">
        <BackgroundBeams className="z-[-1]"/>
        <div className="flex flex-col gap-6 p-12 rounded-xl bg-black/90 w-4/5 sm:max-w-96 mx-auto text-white sm:text-2xl">
          <h1>Welcome to SMIP</h1> 
          <h1>A stock market inspired game where you can invest in your favorite social media posts</h1>
          <Button className="mx-auto justify-center items-center mt-2 mb-4 font-bold">
            <Link href="/home"> Enter SMIP </Link>
          </Button>
          <div className="w-1/6 mx-auto">
            <Link href="https://github.com/rithkott/SMIP">
              <Image 
                src="/images/github-mark-white.svg" 
                alt="Link to Github"
                layout="responsive" 
                className="rounded-lg mx-auto"
                width={50}
                height={50}
                />
            </Link>
          </div>
        </div>

      </main>
    </div>
  );
}
