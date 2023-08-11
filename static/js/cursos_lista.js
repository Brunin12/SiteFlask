
function exibirConfirmacao(cursoId) {
    Swal.fire({
        title: 'Tem certeza?',
        text: 'Você está prestes a excluir o curso. Essa ação não pode ser desfeita.',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sim, excluir',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            // Se o usuário clicou em "Sim, excluir", redirecionar para a rota de exclusão do curso
            window.location.href = '/' + cursoId + '/excluir_curso';
        }
    });
}
