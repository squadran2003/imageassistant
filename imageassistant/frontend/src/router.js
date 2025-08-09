

import { createWebHistory, createRouter } from 'vue-router'

import IndexPage from './components/IndexPage.vue';
import LoginForm from './components/auth/LoginForm.vue';
import LogOut from './components/auth/LogOut.vue';
import ResetPassword from './components/auth/ResetPassword.vue';
import SignUp from './components/auth/SignUp.vue';
import PasswordResetConfirm from './components/auth/PasswordRestConfirm.vue';
import CreateImage  from './components/image/CreateImage.vue';
import RemoveBackground from './components/image/RemoveBackground.vue';
import CreateGrayscale from './components/image/CreateGrayscale.vue';
import CreateOutline from './components/image/CreateOutline.vue';
import UserImages from './components/user/UserImages.vue';
import FAQ from './components/FAQ.vue';
import Contact from './components/Contact.vue';
import PrivacyPolicy from './components/PrivacyPolicy.vue';
import Prices from './components/Prices.vue';  
import TermsAndConditions from './components/TermsAndConditions.vue';
import StripeCheckout from './components/payment/StripeCheckout.vue';

const routes = [
  { path: '/', component: IndexPage },
  { path: '/users/login', component: LoginForm },
  { path: '/users/logout', component: LogOut },
  { path: '/users/change/password', component: ResetPassword },
  { path: '/users/signup', component: SignUp },
  { path: '/users/reset/password/confirm/:uidb64/:token/', component: PasswordResetConfirm },
  { path: '/generate/image/', component: CreateImage },
  { path: '/remove/background/', component: RemoveBackground },
  { path: '/create/grayscale/', component: CreateGrayscale },
  { path: '/create/outline/', component: CreateOutline },
  { path: '/users/images/', component: UserImages },
  { path: '/faq', component: FAQ },
  { path: '/contact', component: Contact },
  { path: '/privacy-policy', component: PrivacyPolicy },
  { path: '/pricing', component: Prices },
  { path: '/terms-conditions', component: TermsAndConditions },
  { path: '/checkout', component: StripeCheckout }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
