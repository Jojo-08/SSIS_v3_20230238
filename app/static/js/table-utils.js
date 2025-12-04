/**
 * Table Utilities - Search functionality
 * Uses jQuery for DOM manipulation
 * Note: Sorting is handled server-side
 */

$(document).ready(function() {
  
  // =====================
  // SEARCH FUNCTIONALITY
  // =====================
  
  $('#searchInput').on('input', function() {
    var searchTerm = $(this).val().toLowerCase().trim();
    
    $('.sortable-table tbody tr').each(function() {
      var rowText = $(this).text().toLowerCase();
      
      if (searchTerm === '' || rowText.includes(searchTerm)) {
        $(this).show();
      } else {
        $(this).hide();
      }
    });
    
    // Update visible count (optional)
    var visibleCount = $('.sortable-table tbody tr:visible').length;
    var totalCount = $('.sortable-table tbody tr').length;
    
    if (searchTerm !== '') {
      $('#searchResultCount').text('Showing ' + visibleCount + ' of ' + totalCount + ' results').show();
    } else {
      $('#searchResultCount').hide();
    }
  });
  
  // Clear search button
  $('#clearSearch').on('click', function() {
    $('#searchInput').val('').trigger('input');
  });
  
});
