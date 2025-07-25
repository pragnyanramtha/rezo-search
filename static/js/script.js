document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    const queryInput = document.getElementById('queryInput');
    const searchButton = document.querySelector('.search-button'); 

    if (searchForm && queryInput && searchButton) {
        queryInput.addEventListener('keydown', function(event) {
            
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();    
                searchButton.click();
            }  
        });
        searchForm.addEventListener('submit', function(event) {
        
            event.preventDefault();

           
            const queryText = document.getElementById('queryInput').value.trim();
            const selectedMode = document.getElementById('modeSelect').value;
            const selectedOutput = document.getElementById('outputSelect').value;

            if (queryText) {
     
                const encodedQuery = encodeURIComponent(queryText);      
                let searchUrl = `/search?query=${encodedQuery}`;
                searchUrl += `&mode=${selectedMode}`;
                searchUrl += `&output=${selectedOutput}`;
                window.location.href = searchUrl;
            }
        });
    }
});