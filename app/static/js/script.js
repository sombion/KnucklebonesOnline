document.querySelectorAll('.opponent-board .column').forEach((column, index) => {
    column.addEventListener('click', () => {
        console.log(`Column ${index + 1} clicked!`);
    });
});
