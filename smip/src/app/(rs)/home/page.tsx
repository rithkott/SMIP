import {getKindeServerSession} from "@kinde-oss/kinde-auth-nextjs/server";

export const metadata = {
    title: "Home Page"
}

export default function Home() {
    validateUser();
    return <h2>Home Page</h2>;
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
