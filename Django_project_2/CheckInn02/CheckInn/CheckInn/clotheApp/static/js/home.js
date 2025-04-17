const priceSlider = document.querySelector('.price-slider');
    const priceValue = document.querySelector('.price-value');
    
    priceSlider.addEventListener('input', function() {
        priceValue.textContent = '$' + this.value;
    });

    // animation on clicking generate
    
    let d_asc=document.querySelector(".cap_img");
    let d_shirt=document.querySelector(".upper_img");
    let d_pants=document.querySelector(".pants_img");
    let d_shoes=document.querySelector(".shoes_img");
    let gen_btn=document.querySelector(".gen_btn");
    let mascot_gif=document.querySelector(".mascot_gif");
    let mascot_main=document.querySelector(".mascot_main")
    let mascot_think=document.querySelector(".mascot_think")
    let display_light=document.getElementById("display_light")
    let display_bg=document.getElementById("display_bg")
    let total_value=document.getElementById("total_value")
    let cart_item_asc_img=document.getElementById("cart_item_asc_img")
    let cart_item_upper_img=document.getElementById("cart_item_upper_img")
    let cart_item_lower_img=document.getElementById("cart_item_lower_img")
    let cart_item_shoes_img=document.getElementById("cart_item_shoes_img")
    let cart_item_asc_price=document.getElementById("cart_item_asc_price")
    let cart_item_upper_price=document.getElementById("cart_item_upper_price")
    let cart_item_lower_price=document.getElementById("cart_item_lower_price")
    let cart_item_shoes_price=document.getElementById("cart_item_shoes_price")
    let total_price=document.getElementById("total_price")
    let cart_details=document.getElementById("cart_details")
    let choose=document.getElementById("choose")
    let choose_l=document.querySelector(".choose_l")
    let logo_img=document.getElementById("logo_img")

    let formData = {
        upper: {},
        lower: {},
        shoes: {},
        accessory: {},
        price: 5000
    };

    let currentOutfitItems = {
        upper: null,
        lower: null,
        shoes: null,
        accessory: null
    };

    gen_btn.addEventListener("click",()=>{
        console.log("Sending formData:", formData);
        console.log("Registered");
        d_asc.style.opacity=1;
        d_shirt.style.opacity=1;
        d_pants.style.opacity=1;
        d_shoes.style.opacity=1;
        d_asc.style.transition="340ms";
        d_shirt.style.transition="340ms";
        d_pants.style.transition="340ms";
        d_shoes.style.transition="340ms";
        mascot_gif.classList.add("mascot_gif_active")
        mascot_main.style.opacity=0;
        mascot_think.style.opacity=1;
        mascot_think.style.transition="340ms";
        mascot_gif.style.transition="340ms";  
        display_light.classList.add("display_light_on")
        display_bg.classList.add("display_bg_on")
        cart_details.style.transition="340ms";
        cart_details.style.opacity=1;
        total_price.style.transition="340ms";
        total_price.style.opacity=1;

        const params = new URLSearchParams({
            price: formData.price,
            upper_type: formData.upper.type || "",
            upper_sizes: (formData.upper.sizes || []).join(","),
            upper_colors: (formData.upper.colors || []).join(","),
            lower_type: formData.lower.type || "",
            lower_sizes: (formData.lower.sizes || []).join(","),
            lower_colors: (formData.lower.colors || []).join(","),
            shoes_type: formData.shoes.type || "",
            shoes_sizes: (formData.shoes.sizes || []).join(","),
            shoes_colors: (formData.shoes.colors || []).join(","),
            accessory_type: formData.accessory.type || "",
            accessory_styles: (formData.accessory.styles || []).join(","),
            accessory_colors: (formData.accessory.colors || []).join(",")
        });
    
        fetch(`/generate/?${params.toString()}`)
            .then(response => response.json())
            .then(data => {
                console.log("Full response from backend:", data);
                console.log("Upper:"+data.upper.id,"Lower:"+data.lower.id,"Shoes:"+data.shoes.id,"Accessory:"+data.accessory.id)
                
                currentOutfitItems.upper = data.upper.id || null;
                currentOutfitItems.lower = data.lower.id || null;
                currentOutfitItems.shoes = data.shoes.id || null;
                currentOutfitItems.accessory = data.accessory.id || null;
            
            document.getElementById('hidden_upper_id').value = currentOutfitItems.upper || '';
            document.getElementById('hidden_lower_id').value = currentOutfitItems.lower || '';
            document.getElementById('hidden_shoes_id').value = currentOutfitItems.shoes || '';
            document.getElementById('hidden_accessory_id').value = currentOutfitItems.accessory || '';
                if (data.upper?.image) d_shirt.src = "../" + data.upper.image;
                if (data.lower?.image) d_pants.src = data.lower.image;
                if (data.shoes?.image) d_shoes.src = data.shoes.image;
                if (data.accessory?.image) d_asc.src = data.accessory.image;
                let sum_price=data.upper.price + data.lower.price + data.shoes.price + data.accessory.price;
                if (data.upper?.image && data.lower?.image && data.shoes?.image && data.accessory?.image )total_value.innerHTML = "$" + sum_price;
                if (data.upper?.image && data.lower?.image && data.shoes?.image && data.accessory?.image ) cart_item_asc_img.src = data.accessory.image;
                if (data.upper?.image && data.lower?.image && data.shoes?.image && data.accessory?.image ) cart_item_upper_img.src = data.upper.image;
                if (data.upper?.image && data.lower?.image && data.shoes?.image && data.accessory?.image ) cart_item_lower_img.src = data.lower.image;
                if (data.upper?.image && data.lower?.image && data.shoes?.image && data.accessory?.image ) cart_item_shoes_img.src = data.shoes.image;
                if (data.upper?.image && data.lower?.image && data.shoes?.image && data.accessory?.image ) cart_item_asc_price.innerHTML = "$" + data.accessory.price;
                if (data.upper?.image && data.lower?.image && data.shoes?.image && data.accessory?.image ) cart_item_upper_price.innerHTML = "$" + data.upper.price;
                if (data.upper?.image && data.lower?.image && data.shoes?.image && data.accessory?.image ) cart_item_lower_price.innerHTML = "$" + data.lower.price;
                if (data.upper?.image && data.lower?.image && data.shoes?.image && data.accessory?.image ) cart_item_shoes_price.innerHTML = "$" + data.shoes.price;
            });
        });
        document.querySelector('.fa-cart-shopping').addEventListener('click', function() {
            window.location.href = '/cart/';
        });
        
    //CSS animation for cart
    document.getElementById('add_cart_all_btn').addEventListener('click', function() {
        const cartIcon = document.querySelector('.fa-cart-plus');
        cartIcon.classList.add('cart-animation');
        setTimeout(() => {
            cartIcon.classList.remove('cart-animation');
        }, 1000);
    });
        
    const style = document.createElement('style');
    style.textContent = `
    .cart-animation {
        animation: bounce 0.5s ease;
        color: #fd9c52;
    }
        
    @keyframes bounce {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.3); }
    }
    `;
     document.head.appendChild(style);

    // Toggle dark/light mode
    document.getElementById('theme-toggle').addEventListener('click', function() {
        document.body.classList.toggle('body_dark');
        document.body.classList.toggle('body_light');
        

        const icon = this.querySelector('i');
        if (icon.classList.contains('fa-moon')) {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
            choose.style.filter = "invert(1) saturate(3)";
            choose_l.style.filter = "invert(1)";
            logo_img.style.filter = "invert(1)";
        } else {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
            choose.style.filter = "invert(0)";
            choose_l.style.filter = "invert(0)";
            logo_img.style.filter = "invert(0)";
        }
    });
    // UpperWear form toggle
    let upperwear = document.querySelector(".s1_1");
    let upper_form = document.getElementById("upper_form");
    let upper_submit = document.getElementById("upper_submit");
    let uw_isactive = false;

    upper_submit.addEventListener("click", (e) => {
        e.preventDefault();
        console.log("UpperWear Submit Clicked");
    
        const upperType = document.getElementById("upper_type").value;
        const upperSizes = Array.from(document.querySelectorAll('input[name^="size_upper_"]:checked')).map(i => i.value);
        const upperColors = Array.from(document.querySelectorAll('input[name="colour_upper"]:checked')).map(i => i.value);
    
        formData.upper = {
            type: upperType,
            sizes: upperSizes,
            colors: upperColors
        };
    
        upper_form.classList.add("upper_form_inactive");
        upper_form.classList.remove("upper_form_active");
        uw_isactive = false;
    });

    upperwear.addEventListener("click", () => {
        console.log("UpperWear Clicked")
        // Close all other forms first
        lowerwear_form.classList.add("lower_form_inactive");
        lowerwear_form.classList.remove("lower_form_active");
        lw_isactive = false;
        
        shoes_form.classList.add("shoes_form_inactive");
        shoes_form.classList.remove("shoes_form_active");
        sw_isactive = false;
        
        accessory_form.classList.add("accessory_form_inactive");
        accessory_form.classList.remove("accessory_form_active");
        ac_isactive = false;
        
        // Toggle upperwear form
        if(!uw_isactive){
            uw_isactive = true;
            upper_form.classList.add("upper_form_active")
            upper_form.classList.remove("upper_form_inactive")
        } else {
            uw_isactive = false;
            upper_form.classList.add("upper_form_inactive")
            upper_form.classList.remove("upper_form_active")
        }
    });
    
    // LowerWear form toggle
    let lowerwear = document.querySelector(".s1_2");
    let lowerwear_form = document.getElementById("lower_form");
    let lower_submit = document.getElementById("lower_submit");
    let lw_isactive = false;
    
    lower_submit.addEventListener("click", (e) => {
        e.preventDefault();
        console.log("LowerWear Submit Clicked");
    
        const lowerType = document.getElementById("lower_type").value;
        const lowerSizes = Array.from(document.querySelectorAll('input[name^="size_lower_"]:checked')).map(i => i.value);
        const lowerColors = Array.from(document.querySelectorAll('input[name="colour_lower"]:checked')).map(i => i.value);
    
        formData.lower = {
            type: lowerType,
            sizes: lowerSizes,
            colors: lowerColors
        };
    
        lowerwear_form.classList.add("lower_form_inactive");
        lowerwear_form.classList.remove("lower_form_active");
        lw_isactive = false;
    });
    
    lowerwear.addEventListener("click", () => {
        console.log("LowerWear Clicked")
        // Close all other forms first
        upper_form.classList.add("upper_form_inactive");
        upper_form.classList.remove("upper_form_active");
        uw_isactive = false;
        
        shoes_form.classList.add("shoes_form_inactive");
        shoes_form.classList.remove("shoes_form_active");
        sw_isactive = false;
        
        accessory_form.classList.add("accessory_form_inactive");
        accessory_form.classList.remove("accessory_form_active");
        ac_isactive = false;
        
        // Toggle lowerwear form
        if(!lw_isactive){
            lw_isactive = true;
            lowerwear_form.classList.add("lower_form_active")
            lowerwear_form.classList.remove("lower_form_inactive")
        } else {
            lw_isactive = false;
            lowerwear_form.classList.add("lower_form_inactive")
            lowerwear_form.classList.remove("lower_form_active")
        }
    });
    
    // Shoes form toggle
    let shoes = document.querySelector(".s1_3");
    let shoes_form = document.getElementById("shoes_form");
    let shoes_submit = document.getElementById("shoes_submit");
    let sw_isactive = false;
    
    shoes_submit.addEventListener("click", (e) => {
        e.preventDefault();
        console.log("Shoes Submit Clicked");
    
        const shoesType = document.getElementById("shoes_type").value;
        const shoesSizes = Array.from(document.querySelectorAll('input[name^="size_shoes_"]:checked')).map(i => i.value);
        const shoesColors = Array.from(document.querySelectorAll('input[name="colour_shoes"]:checked')).map(i => i.value);
    
        formData.shoes = {
            type: shoesType,
            sizes: shoesSizes,
            colors: shoesColors
        };
    
        shoes_form.classList.add("shoes_form_inactive");
        shoes_form.classList.remove("shoes_form_active");
        sw_isactive = false;
    });
    
    shoes.addEventListener("click", () => {
        console.log("Shoes Clicked")
        // Close all other forms first
        upper_form.classList.add("upper_form_inactive");
        upper_form.classList.remove("upper_form_active");
        uw_isactive = false;
        
        lowerwear_form.classList.add("lower_form_inactive");
        lowerwear_form.classList.remove("lower_form_active");
        lw_isactive = false;
        
        accessory_form.classList.add("accessory_form_inactive");
        accessory_form.classList.remove("accessory_form_active");
        ac_isactive = false;
        
        // Toggle shoes form
        if(!sw_isactive){
            sw_isactive = true;
            shoes_form.classList.add("shoes_form_active")
            shoes_form.classList.remove("shoes_form_inactive")
        } else {
            sw_isactive = false;
            shoes_form.classList.add("shoes_form_inactive")
            shoes_form.classList.remove("shoes_form_active")
        }
    });
    
    // Accessories form toggle
    let accessories = document.querySelector(".s2_1");
    let accessory_form = document.getElementById("accessory_form");
    let accessory_submit = document.getElementById("accessory_submit");
    let ac_isactive = false;
    
    accessory_submit.addEventListener("click", (e) => {
        e.preventDefault();
        console.log("Accessories Submit Clicked");
    
        const accessoryType = document.getElementById("accessory_type").value;
        const accessoryStyles = Array.from(document.querySelectorAll('input[name^="style_accessory_"]:checked')).map(i => i.value);
        const accessoryColors = Array.from(document.querySelectorAll('input[name="colour_accessory"]:checked')).map(i => i.value);
    
        formData.accessory = {
            type: accessoryType,
            styles: accessoryStyles,
            colors: accessoryColors
        };
    
        accessory_form.classList.add("accessory_form_inactive");
        accessory_form.classList.remove("accessory_form_active");
        ac_isactive = false;
    });
    
    accessories.addEventListener("click", () => {
        console.log("Accessories Clicked")
        // Close all other forms first
        upper_form.classList.add("upper_form_inactive");
        upper_form.classList.remove("upper_form_active");
        uw_isactive = false;
        
        lowerwear_form.classList.add("lower_form_inactive");
        lowerwear_form.classList.remove("lower_form_active");
        lw_isactive = false;
        
        shoes_form.classList.add("shoes_form_inactive");
        shoes_form.classList.remove("shoes_form_active");
        sw_isactive = false;
        
        // Toggle accessories form
        if(!ac_isactive){
            ac_isactive = true;
            accessory_form.classList.add("accessory_form_active")
            accessory_form.classList.remove("accessory_form_inactive")
        } else {
            ac_isactive = false;
            accessory_form.classList.add("accessory_form_inactive")
            accessory_form.classList.remove("accessory_form_active")
        }
    });