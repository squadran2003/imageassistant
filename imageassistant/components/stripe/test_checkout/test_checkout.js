(function(){
    const stripe = Stripe("pk_test_51Q99SfJfXU0eN0TRNZrQeZvpOACUdVjGR7RaMISSaML0I1cHhrTKEX1eTl1B47xPnlFS23fLsXCpBCzWdozwKmMv00pkyGng9A");
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