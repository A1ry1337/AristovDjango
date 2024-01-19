function toggleMenu() {
  const menu = document.getElementById('menu');
  const content = document.getElementById('content');
  const isOpen = menu.style.left === '0px';

  menu.style.left = isOpen ? '-300px' : '0px';
  content.style.marginLeft = isOpen ? '0' : '250px';
}
