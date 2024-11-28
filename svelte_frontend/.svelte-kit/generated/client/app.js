export { matchers } from './matchers.js';

export const nodes = [
	() => import('./nodes/0'),
	() => import('./nodes/1'),
	() => import('./nodes/2'),
	() => import('./nodes/3'),
	() => import('./nodes/4'),
	() => import('./nodes/5'),
	() => import('./nodes/6'),
	() => import('./nodes/7'),
	() => import('./nodes/8'),
	() => import('./nodes/9'),
	() => import('./nodes/10'),
	() => import('./nodes/11'),
	() => import('./nodes/12'),
	() => import('./nodes/13')
];

export const server_loads = [];

export const dictionary = {
		"/": [4],
		"/student/[username]": [5,[2]],
		"/student/[username]/results": [6,[2]],
		"/student/[username]/results/[test_id]": [7,[2]],
		"/student/[username]/tests": [8,[2]],
		"/student/[username]/tests/[test_id]": [9,[2]],
		"/teacher/[username]": [10,[3]],
		"/teacher/[username]/createTest": [11,[3]],
		"/teacher/[username]/tests": [12,[3]],
		"/teacher/[username]/tests/[test_id]": [13,[3]]
	};

export const hooks = {
	handleError: (({ error }) => { console.error(error) }),

	reroute: (() => {})
};

export { default as root } from '../root.js';