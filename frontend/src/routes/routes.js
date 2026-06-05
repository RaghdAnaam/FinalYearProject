import LandingPage from '../pages/landing/index.vue';
import LoginPage from '../pages/login/index.vue';
import RegistrationPage from '../pages/register/index.vue';
import Dashboard from '../pages/dashboard/index.vue';
import Skin from '../pages/skin/index.vue';
import routines from '../pages/routines/index.vue';
import photoHistory from '../pages/photoHistory.vue';
import analysisHistory from '../pages/analysis/index.vue';
import adminLogin from '../pages/admin/login.vue';
import adminDashboard from '../pages/admin/dashboard.vue';
import adminUsers from '../pages/admin/users.vue';
import ResetPassword from '../pages/password/ResetPassword.vue';
import ForgotPassword from '../pages/password/ForgotPassword.vue';


const routes = [
	{
		path: '/',
		component: LandingPage,
		name: 'route-landing',
		meta: { layout: 'landing' },
	},
	{
		path: '/login',
		component: LoginPage,
		name: 'route-login',
		meta: { layout: 'LogReg' },
	},
	{
		path: '/register',
		component: RegistrationPage,
		name: 'route-register',
		meta: { layout: 'LogReg' },
	},
	{
		path: '/dashboard',
		component: Dashboard,
		name: 'route-dashboard',
		meta: { layout: 'Dashboard' },
	},
	{
		path: '/dashboard/progress',
		component: Skin,
		name: 'route-skin',
		meta: { layout: 'Dashboard' },
	},
	{
		path: '/dashboard/routines',
		component: routines,
		name: 'route-routines',
		meta: { layout: 'Dashboard' },
	},
	{
		path: '/dashboard/history',
		component: photoHistory,
		name: 'route-photo-history',
		meta: { layout: 'Dashboard' },
	},
	{
		path: '/dashboard/analysis',
		component: analysisHistory,
		name: 'route-analysis',
		meta: { layout: 'Dashboard' },
	},
	{
		path: '/admin/login',
		component: adminLogin,
		name: 'route-admin-login',
		meta: { layout: 'LogReg' },
	},
	{
		path: '/admin/dashboard',
		component: adminDashboard,
		name: 'route-admin-dashbboard',
		meta: { layout: 'admin' },
	},
	{
		path: '/admin/users',
		component: adminUsers,
		name: 'route-admin-users',
		meta: { layout: 'admin' },
	},
	{
		path: '/forgot-password',
		component: ForgotPassword,
		name: 'route-forgot-password',
		meta: { layout: 'LogReg' },
	},
	{
		path: '/reset-password',
		component: ResetPassword,
		name: 'route-reset-password',
		meta: { layout: 'LogReg' },
	},
	
	
	  
];

export default routes;
