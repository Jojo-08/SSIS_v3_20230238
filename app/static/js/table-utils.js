/**
 * Table Utilities - Search and Sort functionality
 * Uses jQuery for DOM manipulation
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
  
  // =====================
  // SORT FUNCTIONALITY
  // =====================
  
  // Initialize sortable headers
  $('.sortable-table thead th').each(function(index) {
    var headerText = $(this).text().trim().toLowerCase();
    
    // Skip non-sortable columns
    if (headerText === 'actions' || headerText === 'photo') {
      return;
    }
    
    // Add sortable class and data attributes
    $(this).addClass('sortable')
           .attr('data-column', index)
           .attr('data-order', 'none')
           .css('cursor', 'pointer');
  });
  
  // Handle sort click
  $('.sortable-table').on('click', 'th.sortable', function() {
    var $table = $(this).closest('table');
    var $headers = $table.find('thead th');
    var columnIndex = $(this).data('column');
    var currentOrder = $(this).data('order');
    var newOrder = (currentOrder === 'asc') ? 'desc' : 'asc';
    
    // Reset all headers
    $headers.removeClass('asc desc').data('order', 'none');
    
    // Set current header
    $(this).addClass(newOrder).data('order', newOrder);
    
    // Sort the table
    sortTable($table, columnIndex, newOrder);
  });
  
  /**
   * Sort table by column
   * @param {jQuery} $table - The table element
   * @param {number} columnIndex - Column index to sort by
   * @param {string} order - 'asc' or 'desc'
   */
  function sortTable($table, columnIndex, order) {
    var $tbody = $table.find('tbody');
    var $rows = $tbody.find('tr').toArray();
    
    $rows.sort(function(a, b) {
      var $aCell = $(a).find('td, th').eq(columnIndex);
      var $bCell = $(b).find('td, th').eq(columnIndex);
      
      var aValue = $aCell.text().trim();
      var bValue = $bCell.text().trim();
      
      // Check if values look like Student IDs (YYYY-NNNN format)
      var studentIdPattern = /^\d{4}-\d{4}$/;
      if (studentIdPattern.test(aValue) && studentIdPattern.test(bValue)) {
        return compareStudentIds(aValue, bValue, order);
      }
      
      // Check if values are numbers
      var aNum = parseFloat(aValue);
      var bNum = parseFloat(bValue);
      
      if (!isNaN(aNum) && !isNaN(bNum)) {
        return order === 'asc' ? aNum - bNum : bNum - aNum;
      }
      
      // Sort as strings (case-insensitive)
      aValue = aValue.toLowerCase();
      bValue = bValue.toLowerCase();
      
      if (order === 'asc') {
        return aValue.localeCompare(bValue);
      } else {
        return bValue.localeCompare(aValue);
      }
    });
    
    // Re-append sorted rows
    $.each($rows, function(index, row) {
      $tbody.append(row);
    });
  }
  
  /**
   * Compare Student IDs in YYYY-NNNN format
   * First compares by year, then by number
   * @param {string} a - First student ID
   * @param {string} b - Second student ID
   * @param {string} order - 'asc' or 'desc'
   * @returns {number} - Comparison result
   */
  function compareStudentIds(a, b, order) {
    var aParts = a.split('-');
    var bParts = b.split('-');
    
    var aYear = parseInt(aParts[0]);
    var bYear = parseInt(bParts[0]);
    var aNum = parseInt(aParts[1]);
    var bNum = parseInt(bParts[1]);
    
    // First compare by year
    if (aYear !== bYear) {
      return order === 'asc' ? aYear - bYear : bYear - aYear;
    }
    
    // If same year, compare by number
    return order === 'asc' ? aNum - bNum : bNum - aNum;
  }
  
});
