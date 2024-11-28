<script lang="ts">
	import '../app.css';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { getInfoFromToken, logout } from '../utils/auth';
	import { isLoading } from '../utils/stores';

	// Logic to handle role based user navigation
	onMount(async () => {
		isLoading.set(true);
		var info = getInfoFromToken();

		const currentPath = window.location.pathname;

		if (!info && currentPath !== "/") {
			await logout();
			isLoading.set(false);
		}

		if (info?.role === "Student" && currentPath.startsWith("/teacher")) {
			goto(`/student/${info.sub}`);
		} else if (info?.role === "Teacher" && currentPath.startsWith("/student")) {
			goto(`/teacher/${info.sub}`);
		}
		isLoading.set(false);
	});
</script>

<div class="layout" style="filter: blur({$isLoading ? '2px' : '0px'})">
    
</div>

<!-- Render the children passed to the layout -->
<slot />
