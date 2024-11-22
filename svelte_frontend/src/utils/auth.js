import { goto } from '$app/navigation';

export async function refreshAccessToken() {
    const access_token = sessionStorage.getItem("access_token");
    const response = await fetch("http://localhost:8000/refresh", {
        method: "POST",
        credentials: "include",
        headers: {
            "Authorization": `Bearer ${access_token}`,
            "Content-Type": "application/json",
        }
    });

    if (response.ok) {
        const data = await response.json();
        sessionStorage.setItem("access_token", data.access_token);
        return data.access_token;
    } else {
        sessionStorage.removeItem("access_token");
        goto("/")
    }
}