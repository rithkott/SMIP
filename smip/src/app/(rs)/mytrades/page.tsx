import {getKindeServerSession} from "@kinde-oss/kinde-auth-nextjs/server";

export const metadata = {
    title: "My Trades"
}

const fetchUserData = async () => {
    const { getUser } = getKindeServerSession();
    const user = await getUser();
    const email: string = user.email!;
    return email
};

const createUser = async (data: string) => {
    const response = await fetch('http://127.0.0.1:5000/api/users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: data , //This is sending only the email not sending a JSON must fix IFH Typescript
    });
    
    console.log(response); 
};

export default async function MyTrades(){
    const data = await fetchUserData();
    createUser(data);

    return <h2>My Trades Page</h2>

}


