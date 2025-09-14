document.addEventListener('DOMContentLoaded', function() {
    console.log('Search script loaded');
    
    const searchInput = document.getElementById('product-search');
    const suggestionsBox = document.getElementById('suggestions-box');
    
    // Debug: Check if elements exist
    console.log('Search input:', searchInput);
    console.log('Suggestions box:', suggestionsBox);
    
    if (!searchInput) {
        console.error('Search input not found');
        return;
    }
    if (!suggestionsBox) {
        console.error('Suggestions box not found');
        return;
    }

    let debounceTimer;
    let popularSearches = [];

    // Load popular searches for autocomplete
    function loadPopularSearches() {
        fetch('/products/popular-searches/')
            .then(response => {
                if (!response.ok) throw new Error('Failed to load popular searches');
                return response.json();
            })
            .then(data => {
                popularSearches = data;
                console.log('Popular searches loaded:', popularSearches);
            })
            .catch(error => {
                console.error('Error loading popular searches:', error);
                // Fallback popular searches
                popularSearches = ["f-sheet", "notebook", "laptop", "accessories", "electronics"];
            });
    }

    // Show autocomplete suggestions (like YouTube)
    function showAutocompleteSuggestions(query) {
        if (!query) {
            suggestionsBox.innerHTML = '';
            suggestionsBox.style.display = 'none';
            return;
        }

        const matchingSearches = popularSearches.filter(term => 
            term.toLowerCase().includes(query.toLowerCase())
        ).slice(0, 5);

        if (matchingSearches.length > 0) {
            suggestionsBox.innerHTML = '';
            matchingSearches.forEach(term => {
                const div = document.createElement('div');
                div.className = 'suggestion-item autocomplete-item';
                div.innerHTML = `
                    <i class="fas fa-search"></i>
                    <span>${term}</span>
                `;
                div.addEventListener('click', () => {
                    searchInput.value = term;
                    suggestionsBox.style.display = 'none';
                    searchInput.focus();
                    // Trigger search
                    const event = new Event('input', { bubbles: true });
                    searchInput.dispatchEvent(event);
                });
                suggestionsBox.appendChild(div);
            });
            suggestionsBox.style.display = 'block';
        } else {
            suggestionsBox.style.display = 'none';
        }
    }

    // Function to show loading state
    function showLoading() {
        suggestionsBox.innerHTML = '<div class="suggestion-loading"><i class="fas fa-spinner fa-spin"></i> Searching...</div>';
        suggestionsBox.style.display = 'block';
    }

    // Function to hide suggestions
    function hideSuggestions() {
        suggestionsBox.style.display = 'none';
    }

    // Function to fetch search suggestions
    function fetchSearchSuggestions(query) {
        showLoading();
        
        console.log('Fetching suggestions for:', query);
        
        fetch(`/products/suggest/?q=${encodeURIComponent(query)}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(suggestions => {
                console.log('Received suggestions:', suggestions);
                displaySearchSuggestions(suggestions, query);
            })
            .catch(error => {
                console.error('Error fetching suggestions:', error);
                suggestionsBox.innerHTML = '<div class="suggestion-error">Error loading suggestions</div>';
            });
    }

    // Function to display search suggestions
    function displaySearchSuggestions(suggestions, query) {
        if (!suggestions || suggestions.length === 0) {
            suggestionsBox.innerHTML = `
                <div class="suggestion-empty">
                    <i class="fas fa-search"></i>
                    <div>No products found for "${query}"</div>
                    <div class="suggestion-try">Try different keywords</div>
                </div>
            `;
            return;
        }

        suggestionsBox.innerHTML = '';
        
        // Add header
        const header = document.createElement('div');
        header.className = 'suggestion-header';
        header.innerHTML = `<span>Products matching "${query}"</span>`;
        suggestionsBox.appendChild(header);

        suggestions.forEach(item => {
            const div = document.createElement('div');
            div.className = 'suggestion-item';
            
            // Highlight matching text
            const highlightedName = highlightText(item.name, query);
            const highlightedStartup = item.startup ? highlightText(item.startup, query) : '';
            
            div.innerHTML = `
                <div class="suggestion-content">
                    <div class="suggestion-name">${highlightedName}</div>
                    ${item.startup ? `<div class="suggestion-startup">${highlightedStartup}</div>` : ''}
                </div>
                <div class="suggestion-arrow"><i class="fas fa-chevron-right"></i></div>
            `;
            
            div.addEventListener('click', () => {
                console.log('Navigating to product:', item.slug);
                window.location.href = `/products/${item.slug}/`;
            });
            
            suggestionsBox.appendChild(div);
        });
    }

    // Highlight matching text in search results
    function highlightText(text, query) {
        if (!query) return text;
        
        try {
            const regex = new RegExp(`(${escapeRegex(query)})`, 'gi');
            return text.replace(regex, '<span class="highlight">$1</span>');
        } catch (e) {
            return text; // Fallback if regex fails
        }
    }

    // Escape special regex characters
    function escapeRegex(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    // Debounce function
    function debounce(func, delay) {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(func, delay);
    }

    // Event listeners
    searchInput.addEventListener('input', function() {
        const query = this.value.trim();
        
        if (query.length === 0) {
            hideSuggestions();
            return;
        }

        if (query.length === 1) {
            // Show autocomplete suggestions for single character
            showAutocompleteSuggestions(query);
        } else if (query.length >= 2) {
            // Fetch actual search results for longer queries
            debounce(() => fetchSearchSuggestions(query), 300);
        }
    });

    searchInput.addEventListener('focus', function() {
        const query = this.value.trim();
        if (query.length === 1) {
            showAutocompleteSuggestions(query);
        } else if (query.length >= 2) {
            // If we already have suggestions, show them
            if (suggestionsBox.children.length > 0) {
                suggestionsBox.style.display = 'block';
            } else {
                // Otherwise fetch new suggestions
                fetchSearchSuggestions(query);
            }
        }
    });

    // Hide suggestions when clicking outside
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !suggestionsBox.contains(e.target)) {
            hideSuggestions();
        }
    });

    // Keyboard navigation
    searchInput.addEventListener('keydown', function(e) {
        const suggestions = suggestionsBox.querySelectorAll('.suggestion-item');
        if (suggestions.length === 0) return;
        
        let activeSuggestion = suggestionsBox.querySelector('.suggestion-item.active');
        
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            if (!activeSuggestion) {
                suggestions[0].classList.add('active');
            } else {
                activeSuggestion.classList.remove('active');
                const next = activeSuggestion.nextElementSibling;
                if (next) next.classList.add('active');
            }
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            if (!activeSuggestion) {
                suggestions[suggestions.length - 1].classList.add('active');
            } else {
                activeSuggestion.classList.remove('active');
                const prev = activeSuggestion.previousElementSibling;
                if (prev) prev.classList.add('active');
            }
        } else if (e.key === 'Enter') {
            if (activeSuggestion) {
                e.preventDefault();
                activeSuggestion.click();
            }
        } else if (e.key === 'Escape') {
            hideSuggestions();
            searchInput.blur();
        }
    });

    // Load popular searches on startup
    loadPopularSearches();
    
    console.log('Search functionality initialized successfully');
});