<script lang="ts">
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
    import { getInfoFromToken, logout } from '../utils/auth';

	export let status: number;

	onMount(async () => {
		var info = getInfoFromToken();

        if (!info){
            await logout();
        } else {
            goto(`/${info.role.charAt(0).toLowerCase() + info.role.slice(1)}/${info.sub}`)
        }
	});
</script>

<p>Error: {status}</p>
