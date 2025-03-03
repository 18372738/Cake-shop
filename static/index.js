Vue.createApp({
    name: "App",
    components: {
        VForm: VeeValidate.Form,
        VField: VeeValidate.Field,
        ErrorMessage: VeeValidate.ErrorMessage,
    },
    data() {
        return {
            schema1: {
                lvls: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' количество уровней';
                },
                form: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' форму торта';
                },
                topping: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' топпинг';
                }
            },
            schema2: {
                name: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' имя';
                },
                phone: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' телефон';
                },
                name_format: (value) => {
                    const regex = /^[a-zA-Zа-яА-Я]+$/
                    if (!value) {
                        return true;
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Формат имени нарушен';
                    }
                    return true;
                },
                email_format: (value) => {
                    const regex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i
                    if (!value) {
                        return true;
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Формат почты нарушен';
                    }
                    return true;
                },
                phone_format:(value) => {
                    const regex = /^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$/
                    if (!value) {
                        return true;
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Формат телефона нарушен';
                    }
                    return true;
                },
                email: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' почту';
                },
                address: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' адрес';
                },
                date: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' дату доставки';
                },
                time: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' время доставки';
                }
            },
            DATA: {
                Levels: cake_elements.size_titles,
                Forms: cake_elements.form_titles,
                Toppings: cake_elements.topping_titles,
                Berries: cake_elements.berry_titles,
                Decors: cake_elements.decor_titles,
            },
            Costs: {
                Levels: cake_elements.size_prices,
                Forms: cake_elements.form_prices,
                Toppings: cake_elements.topping_prices,
                Berries: cake_elements.berry_prices,
                Decors: cake_elements.decor_prices,
                Words: 0
            },
            Levels: 0,
            Form: 0,
            Topping: 0,
            Berries: 0,
            Decor: 0,
            Words: '',
            Comments: '',
            Designed: false,

            Name: '',
            Phone: null,
            Email: null,
            Address: null,
            Dates: null,
            Time: null,
            DelivComments: ''
        }
    },
    methods: {
        ToStep4() {
            this.Designed = true
            setTimeout(() => this.$refs.ToStep4.click(), 0);
        },
        redirectToPayment() {
            let cost = this.Cost;
            if (!cost) {
                alert("Стоимость заказа не рассчитана!");
                return;
            }
            let params = new URLSearchParams({
                total_cost: cost,
                phone: this.Phone || '',
                customer_name: this.Name || '',
                email: this.Email || '',
                address: this.Address || '',
                date: this.Dates || '',
                time: this.Time || '',
                comment: this.Comments || '',
                deliv_comments: this.DelivComments || '',
                inscription: this.Words || '',
                levels: this.Levels || 0,
                form: this.Form || 0,
                topping: this.Topping || 0,
                berries: this.Berries || 0,
                decor: this.Decor || 0
            });
            window.location.href = `/create-payment/?${params.toString()}`;
        }
    },
    computed: {
        Cost() {
          let W = this.Words ? (this.Costs.Words || 0) : 0;
          let baseCost =
              (this.Costs.Levels[this.Levels] || 0) +
              (this.Costs.Forms[this.Form] || 0) +
              (this.Costs.Toppings[this.Topping] || 0) +
              (this.Costs.Berries[this.Berries] || 0) +
              (this.Costs.Decors[this.Decor] || 0) + W;

          if (this.Words) {
              baseCost += 500;
          }

          if (this.Dates && this.Time) {
              let orderDateTime = new Date(`${this.Dates}T${this.Time}`);
              let now = new Date();
              let hoursDiff = (orderDateTime - now) / (1000 * 60 * 60);

              if (hoursDiff < 24) {
                  baseCost *= 1.2;
              }
          }

          return Math.round(baseCost);
        }
    }
}).mount('#VueApp')
