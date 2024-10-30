(function(){
    const stripePublicKey = document.querySelector("#stripe_public_key").value;
    const stripe = Stripe(stripePublicKey);
    const token = document.querySelector("#csrfmiddlewaretoken").value;
    const service_id = document.querySelector("#service_id").value;
    const image_id = document.querySelector("#image_id").value;
    initialize();

    // Create a Checkout Session
    async function initialize() {
        const fetchClientSecret = async () => {
            const response = await fetch(`/images/create/checkout/session/${service_id}/${image_id}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": token,
                },
            });
            const { clientSecret } = await response.json();
            return clientSecret;
        };

        const checkout = await stripe.initEmbeddedCheckout({
            fetchClientSecret,
        });

        // Mount Checkout
        checkout.mount('#checkout');
    }
})()     