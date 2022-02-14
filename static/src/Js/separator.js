var input = this.$el.html();

var output = input.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".")