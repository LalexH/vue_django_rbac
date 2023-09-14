import axios from "@/api/http"
import store from "@/store/index"
import router from "@/router/index"

export default {
    login: (data) => axios({
        url: "/api/login",
        method: "POST",
        data: data  
    }),

    userInfo: () => {
        axios.get('/api/userinfo').then((resp)=>{
            localStorage.setItem("userInfo", JSON.stringify(resp.data))
            store.commit("userInfo")
            return resp.data
          }).catch(()=>{
            localStorage.clear();
            router.push("/login/")
            })
    },

    user: (method, data, lookup=null) => {
        var url = lookup ? '/api/user' + '/' + lookup : '/api/user';

        if(method === "GET" && data !== {}){
            url = url + "?" 
            for(var key in data){
                url = url + key + "=" + data[key]    
            }
        }
        return axios({
            url: url,
            method: method,
            data: data,
        })
    },

    menu: (method, data, lookup=null) => {
        var url = lookup ? '/api/menu' + '/' + lookup : '/api/menu';

        if(method === "GET" && data !== {}){
            url = url + "?" 
            for(var key in data){
                url = url + key + "=" + data[key]    
            }
        }
        return axios({
            url: url,
            method: method,
            data: data,
        })
    },

    role: (method, data, lookup=null) => {
        var url = lookup ? '/api/role' + '/' + lookup : '/api/role';

        if(method === "GET" && data !== {}){
            url = url + "?" 
            for(var key in data){
                url = url + key + "=" + data[key]    
            }
        }

        return axios({
            url: url,
            method: method,
            data: data,
        })
    },
    
    permission: (method, data, lookup=null) => {
        var url = lookup ? '/api/permission' + '/' + lookup : '/api/permission';

        if(method === "GET" && data !== {}){
            url = url + "?" 
            for(var key in data){
                url = url + key + "=" + data[key]    
            }
        }
        return axios({
            url: url,
            method: method,
            data: data,
        })
    }
}

