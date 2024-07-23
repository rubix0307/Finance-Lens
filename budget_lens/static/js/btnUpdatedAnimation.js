function updateButtonText(element) {
    const submitButton = element.querySelector('button[type="submit"]');

    if (submitButton) {
        const originalText = submitButton.textContent;
        submitButton.classList.add('btn-updated');

        let savedText = submitButton.getAttribute('data-savedText')
        let defaultText = submitButton.getAttribute('data-defaultText')
        submitButton.textContent = savedText;

        setTimeout(() => {
            submitButton.textContent = defaultText;
        }, 2970);

    }
}