// Flutterwave webhook handler (Express). Deliberately insecure.
app.post('/webhooks/flutterwave', async (req, res) => {
  const event = req.body;
  if (event.data.status === 'successful') {
    const order = await Order.findById(event.data.tx_ref);
    order.status = 'paid';
    order.paidAmount = event.data.amount; // trusts amount from payload
    await order.save();
  }
  console.log('webhook', JSON.stringify(req.headers)); // logs headers incl. verif-hash
  res.sendStatus(200);
});
