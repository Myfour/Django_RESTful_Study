let cp = new Vue({
    el: '#app',
    data: function () {
        return {
            message: 'hello Vue!'
        }
    }
})

let cp2 = new Vue({
    el: '#app2',
    template: '<h1>{{ message }}</h1>',
    data: function () {
        return {
            message: 'Hello Component 2!'
        }
    }
})

//　未使用el属性，则是一个未挂载的实例
let cp3 = new Vue({
    template: `
    <h2>{{message}}</h2>
    `,
    data: function () {
        return {
            message: 'Hello Component 3!'
        }
    }
})
// 使用$mount挂载到元素上
cp3.$mount('#app3')

// 局部注册组件
// Vue 2.x的局部组件的注册不同1.x
let cp4 = {
    template: '<h1>{{message}}</h1>',
    data: function () {
        return {
            message: 'Hello'
        }
    }
}



let cp5 = new Vue({
    el: '#app5',
    template: `
    <div class="text-center">
    {{msg}}
    <cp-4></cp-4>
    </div>
    `,
    components: {
        'cp-4': cp4
    },
    data: function () {
        return {
            msg: 'I\'m Component 5!'
        }
    }
})

// 全局注册组件
Vue.component('global-cp', {
    template: `<h1>{{msg}}</h1>`,
    data: function () {
        return {
            msg: 'I\'m global'
        }
    }

})

let cp6 = new Vue({
    el: '#app6',
    template: `
    <div>
        i'm app6
        <global-cp></global-cp>
    </div>`,
})

let cp7 = new Vue({
    el: '#app7',
    template: `
    <div>
        <global-cp></global-cp>
        {{msg}}
    </div>
    `,
    data: function () {
        return {
            msg: 'I\'m app7'
        }
    }
})