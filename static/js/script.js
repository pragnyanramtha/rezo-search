document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    
    // Check if the form exists on the page
    if (searchForm) {
        searchForm.addEventListener('submit', function(event) {
            // Prevent the form from submitting the traditional way
            event.preventDefault();

            // Get values from the form elements
            const queryText = document.getElementById('queryInput').value.trim();
            const selectedMode = document.getElementById('modeSelect').value;
            const selectedOutput = document.getElementById('outputSelect').value;

            if (queryText) {
                // Encode the query to handle special characters
                const encodedQuery = encodeURIComponent(queryText);
                
                // Start building the URL
                let searchUrl = `/search?query=${encodedQuery}`;
                
                // Add the mode parameter
                searchUrl += `&mode=${selectedMode}`;
                
                // Add the output parameter
                searchUrl += `&output=${selectedOutput}`;
                
                // Redirect the browser to the new URL
                window.location.href = searchUrl;
            }
        });
    }
});