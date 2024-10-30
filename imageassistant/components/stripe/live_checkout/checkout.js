(function(){
    const stripe = Stripe("pk_live_51Q99SfJfXU0eN0TRclOfyyEQcv1oQQW6GsvIcUFPPte5MXmONJmke9yruSszrtDkUhnmZ3fv6llqY2TBX08Q5DQf00atEnBI6p");
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