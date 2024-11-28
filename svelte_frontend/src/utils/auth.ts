import { goto } from '$app/navigation';
import { jwtDecode } from 'jwt-decode';

interface CustomJwtPayload {
    sub: string;
    role: string;
    exp: number;
}

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

export function getInfoFromToken() {
    const token = sessionStorage.getItem('access_token');
    if (!token) return null;
  
    try {
      const decoded = jwtDecode<CustomJwtPayload>(token);
      return {
        sub: decoded.sub,
        role: decoded.role
      };
    } catch (error) {
      return null;
    }
  }
  
  export async function logout() {
    try {
      const response = await fetch("http://localhost:8000/logout", {
        method: "POST",
        credentials: "include"
      });
  
      sessionStorage.removeItem("access_token");
  
      if (response.ok) {
        goto('/');
      } else {
        const responseData = await response.json();
        console.error('Logout failed:', responseData.detail);
        goto('/');
      }
  
    } catch (error) {
      sessionStorage.removeItem("access_token");
      goto("/");
    }
  }
  