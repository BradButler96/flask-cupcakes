$('.delete-cupcake').click(deleteCupcake)

async function deleteCupcake() {
  const id = $(this).data('id')
  await axios.delete(`/api/cupcakes/${ id }`)
  $(this).parent().parent().parent().remove()
}

$('#add-cupcake-btn').click(toggleForm)
$('#cancel-cupcake-btn').click(toggleForm)
$('#submit-cupcake-btn').click(toggleForm)

function toggleForm() {
  $('#form-container').slideToggle()
  $('#add-cupcake').slideToggle()
}
