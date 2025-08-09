<script>

export default {
    name: 'LogOut',
    props: {
        setIsAuthenticated: {
            type: Function,
            required: true
        }
    },
    mounted() {
        this.logout();
    },
    methods: {
        async logout() {
            try {
                this.setIsAuthenticated(false);
                localStorage.removeItem('imageassistant_access_token'); // Clear token from local storage
                this.$router.push('/users/login'); // Redirect to login page
            } catch (error) {
                console.error('Logout error:', error);
            }
        }
    }
};
</script>
