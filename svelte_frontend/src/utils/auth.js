import { goto } from '$app/navigation';

export async function refreshAccessToken() {
    const response = await fetch("http://localhost:8000/refresh", {
        method: "POST",
        credentials: "include",
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