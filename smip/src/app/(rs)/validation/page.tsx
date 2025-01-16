'use server'
import {getKindeServerSession} from "@kinde-oss/kinde-auth-nextjs/server";
import { redirect } from 'next/navigation'
 
export default async function createPost() {
  validateUser()
  redirect('/home') // Navigate to the new post page
}

async function validateUser(): Promise<void> {
  const {getUser} = getKindeServerSession();
  const user = await getUser();
  const usernamevar = user["username"]
  const emailvar = user["email"]
  const url = `http://127.0.0.1:5000/api/users/${emailvar}`
  return fetch(url, {
  method: 'GET',
  headers: { 
  },
  })
  
  .then(response => {
      if (response.status === 404){
          const payload = {username: usernamevar, email: emailvar}
          fetch('http://127.0.0.1:5000/api/users', {
              method: 'POST',
              headers: { 
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify(payload)
          })
          console.log("User Created")
      } else {
          console.log("User Already Validated");
      }
  })
}
