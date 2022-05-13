// Function to delete golf course
function deleteGolfcourse(golfcourseId) {
  console.log("Delete Golfcourse Called");
  fetch("/delete-course", {
    method: "POST",
    body: JSON.stringify({ golfcourseId: golfcourseId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

// Function to delete user
function deleteUser(userId) {
  console.log("Delete User Called");
  fetch("/delete-user", {
    method: "POST",
    body: JSON.stringify({ userId: userId }),
  }).then((_res) => {
    window.location.href = "/users";
  });
}

// Function to filter table values
const table = document.getElementById("courseTable");
// save all tr
const tr = table.getElementsByTagName("tr");

function searchData() {
  //var name = document.getElementById("idName").value.toUpperCase();
  var status = document.getElementById("idStatus").value.toUpperCase();
  var land = document.getElementById("idLand").value.toUpperCase();
  var region = document.getElementById("idRegion").value.toUpperCase();

  for (i = 0; i < tr.length; i++) {
    /*
    var rowName = tr[i].getElementsByTagName("td")[0].textContent.toUpperCase();
    */
    var rowStatus = tr[i]
      .getElementsByTagName("td")[3]
      .textContent.toUpperCase();
    var rowLand = tr[i].getElementsByTagName("td")[2].textContent.toUpperCase();
    var rowRegion = tr[i]
      .getElementsByTagName("td")[1]
      .textContent.toUpperCase();

    var isDisplay = true;

    /*
    if (name != "Bana" && rowName != name) {
      isDisplay = false;
    }
    */
    if (status != "STATUS" && rowStatus != status) {
      isDisplay = false;
    }
    if (land != "LAND" && rowLand != land) {
      isDisplay = false;
    }

    if (region != "REGION" && rowRegion != region) {
      isDisplay = false;
    }

    if (isDisplay) {
      tr[i].style.display = "";
    } else {
      tr[i].style.display = "none";
    }
  }
}

// Function to sort table
function sortTable(n) {
  var table,
    rows,
    switching,
    i,
    x,
    y,
    shouldSwitch,
    dir,
    switchcount = 0;
  table = document.getElementById("courseTable");
  switching = true;
  // Set the sorting direction to ascending:
  dir = "asc";
  /* Make a loop that will continue until
  no switching has been done: */
  while (switching) {
    // Start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /* Loop through all table rows (except the
    first, which contains table headers): */
    for (i = 0; i < rows.length - 1; i++) {
      // Start by saying there should be no switching:
      shouldSwitch = false;
      /* Get the two elements you want to compare,
      one from current row and one from the next: */
      x = rows[i].getElementsByTagName("td")[n];
      y = rows[i + 1].getElementsByTagName("td")[n];
      /* Check if the two rows should switch place,
      based on the direction, asc or desc: */
      if (dir == "asc") {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      /* If a switch has been marked, make the switch
      and mark that a switch has been done: */
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      // Each time a switch is done, increase this count by 1:
      switchcount++;
    } else {
      /* If no switching has been done AND the direction is "asc",
      set the direction to "desc" and run the while loop again. */
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}
