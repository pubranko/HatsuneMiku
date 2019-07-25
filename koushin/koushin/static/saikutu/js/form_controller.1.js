//s = searchの略
var s_count = 1;  //サーチ数の初期値
var grp_count = 1;  //グループ数の初期値

/**入力フォームを追加する関数。
 * 同時に追加用のボタンを下に追加する。
 */
function f_input_form_add(mydocument,s_num){
    s_count += 1;
    //formタグを作成し、条件フィールドと条件追加ボタンを中に設定する。
    let s = document.createElement('form'); 
    s.action = ""; 
    s.method ="GET";
    s.name ="s_input"+s_count;
    s.className="cls_s cls_grp_elem cls_s"+s_count;
    s.innerHTML =   '<select name="Filed">'+
                    '<option value="0" selected>件名＆本文</option>'+
                    '<option value="1">件名</option>'+
                    '<option value="2">本文</option>'+
                    '<option value="3">記事公開日</option>'+
                    '</select> '+
                    '<input type="text" name="s_title'+s_count+'" value=""> '+
                    '<input type="checkbox" name="search_option" value="not_search">not '+
                    '<input type="button" value="条件削除" class="cls_button_control1" onclick="f_input_s_delete(document,'+s_count+')">';
    let s_add = document.createElement('form'); 
    s_add.action = ""; 
    s_add.method ="GET";
    s_add.name ="s_add"+s_count;
    s_add.className="cls_s cls_grp_elem cls_s"+s_count;
    s_add.innerHTML ='<input type="button" value="条件追加" class="cls_button_control1" onclick="f_input_form_add(document,'+s_count+')">';

    for(let ar of mydocument.getElementsByName("s_add"+s_num)){
        ar.parentNode.insertBefore(s_add, ar.nextSibling); 
        ar.parentNode.insertBefore(s, ar.nextSibling); 
    }
}

/**入力フォームを削除する。同時に下にある追加用ボタンを削除する。
 */
function f_input_s_delete(mydocument,s_num){
    let get_forms = mydocument.getElementsByName("s_input"+s_num);
    get_forms[0].parentNode.removeChild(get_forms[0]);
    get_forms = mydocument.getElementsByName("s_add"+s_num);
    get_forms[0].parentNode.removeChild(get_forms[0]);
}

//==================================================================
//以下、グループ操作系
//==================================================================
/**グループ編集 on */
function f_group_control_mode_on(mydocument){
    mydocument.getElementsByName("group_control_mode_on")[0].hidden = true;
    mydocument.getElementsByName("group_control_mode_off")[0].hidden = false;
    //mydocument.getElementsByName("group_edit_mode_on")[0].hidden = true;
    //mydocument.getElementsByName("group_edit_mode_off")[0].hidden = false;

    f_group_add_mode_on(mydocument);
    f_group_edit_mode_on(mydocument);
}
/**グループ編集 off */
function f_group_control_mode_off(mydocument){
    mydocument.getElementsByName("group_control_mode_on")[0].hidden = false;
    mydocument.getElementsByName("group_control_mode_off")[0].hidden = true;
    //mydocument.getElementsByName("group_edit_mode_on")[0].hidden = false;
    //mydocument.getElementsByName("group_edit_mode_off")[0].hidden = true;

    f_group_add_mode_off(mydocument);
    f_group_edit_mode_off(mydocument);
}


/**各フォームをグループとして結合するためのチェックボックスを追加する。*/
function f_group_add_mode_on(mydocument){
    
    let get_forms = mydocument.getElementsByTagName("form");
    let chk_box_add = new Array(get_forms.length);
    for(let i = get_forms.length - 1; i >= 0; i--){
        if (get_forms[i].name.substring(0,7) == "s_input"){
            chk_box_add[i] = document.createElement('input'); 
            chk_box_add[i].type = "checkbox"; 
            chk_box_add[i].name ="grp_select";
            chk_box_add[i].className=get_forms[i].className;
            chk_box_add[i].setAttribute('onclick', "f_group_check(document)");
            get_forms[i].parentNode.insertBefore(chk_box_add[i], get_forms[i]);
        }
    }
    //コントロール系のボタンの表示／非表示と、有効／無効を調整
    mydocument.getElementsByName("group_add_and")[0].hidden = false;
    mydocument.getElementsByName("group_add_or")[0].hidden = false;
    for(let get_cls of mydocument.getElementsByClassName("cls_button_control1")){
        get_cls.disabled = "disabled";
    }
}

/**各フォームをグループとして結合するためのチェックボックスを削除する。*/
function f_group_add_mode_off(mydocument){
    
    let get_forms = mydocument.getElementsByName("grp_select");

    for(let i = get_forms.length - 1; i >= 0; i--){
        get_forms[i].parentNode.removeChild(get_forms[i]);
    }

    //コントロール系のボタンの表示／非表示と、有効／無効を調整
    mydocument.getElementsByName("group_add_and")[0].hidden = true;
    mydocument.getElementsByName("group_add_and")[0].disabled = "disabled";
    mydocument.getElementsByName("group_add_or")[0].hidden = true;
    mydocument.getElementsByName("group_add_or")[0].disabled = "disabled";
    for(let get_cls of mydocument.getElementsByClassName("cls_button_control1")){
        get_cls.disabled = "";
    }
}

/**グループモードでチェックされている数≧2の場合、他のチェックボックスは選択不可にする。
 * また、グループモードonボタンを押下可能にする。
 * それ以外の場合、逆の操作を行う。
 */
function f_group_check(mydocument){
    
    let get_chkboxes = mydocument.getElementsByName("grp_select");
    let grp_chkbox_count =0;

    //チェックされている数を確認
    for (let get_chkbox of get_chkboxes){if(get_chkbox.checked){grp_chkbox_count++}}
    
    //2以上はその他を選択不可に、2未満は全て選択可能にする。
    if(grp_chkbox_count >= 2){
        for (let get_chkbox of get_chkboxes){
            if(get_chkbox.checked){continue}else{get_chkbox.disabled="disabled";}
        }
        mydocument.getElementsByName("group_add_and")[0].disabled = "";
        mydocument.getElementsByName("group_add_or")[0].disabled = "";
    }else{
        for (let get_chkbox of get_chkboxes){get_chkbox.disabled="";}
        mydocument.getElementsByName("group_add_and")[0].disabled = "disabled";
        mydocument.getElementsByName("group_add_or")[0].disabled = "disabled";
    }
}

/**選択されたチェックボックスの間の要素をグループ化する*/
function f_group_add(mydocument,conjunction){
    //グループ化する要素を取得する。
    let get_grp_elem = mydocument.getElementsByClassName("cls_grp_elem");

    /*グループ化可能な要素より、チェックボックスが選択されている範囲を調査する。
      S：チェックボックスが選択されているスタートを調査中。
      E：チェックボックスが選択されているエンドを調査中。
    */
    let i_mode = 'S';
    let pos = new Object(); //連想配列を作成
    for(let i = 0; i < get_grp_elem.length ; i++){
        if(get_grp_elem[i].name=="grp_select" && get_grp_elem[i].checked){
            if(i_mode == 'S'){
                pos["start"] = i;
                i_mode = 'E';
            }else if(i_mode == 'E'){
                pos["end"] = i + 2;   //+2は、チェックボックスの次にある入力フィールドとADDボタンを含めるため。
            }
        }
    }

    //グループタグを、選択されている最初のチェックボックスの前に追加
    grp_count++
    let grp_tag = document.createElement('fieldset'); 
    grp_tag.className ='cls_group '+ 'cls_group_'+conjunction;  //conjunctionにはandかorが入っている。
    grp_tag.name = 'group_'+grp_count;
    grp_tag.innerHTML ='<legend>グループ'+grp_count+' ('+conjunction+'結合)'+'</legend>';
    get_grp_elem[pos["start"]].parentNode.insertBefore(grp_tag, get_grp_elem[pos["start"]]);
    
    //追加したグループタグに、グループ化対象となる要素を移動。
    for(i = pos["start"]; i <= pos["end"] ; i++){
        //console.log("get_grp_elem[i]:"+get_grp_elem[i]);
        grp_tag.appendChild(get_grp_elem[i]);
    }

    //最後に、全てのチェックボックスを、非選択＆選択可能にする。
    let get_chkboxes = mydocument.getElementsByName("grp_select");
    for (let get_chkbox of get_chkboxes){
        get_chkbox.checked = false;
        get_chkbox.disabled = "";
    }

    f_group_check(mydocument);

    //追加後に、グループのリストを最新化。グループモードのon/offの機能で代用。
    f_group_edit_mode_off(mydocument);
    f_group_edit_mode_on(mydocument);
}

/**グループの削除のためのリストをチェックボックスで作る。
 */
function f_group_edit_mode_on(mydocument){

    //グループの数の確認と、グループのリストを作成。
    let get_grp_elem = mydocument.getElementsByClassName("cls_group");
    let get_control = mydocument.getElementsByName("controller_form");
    //グループ数の配列とインデックスを作成
    let edit_label = new Array(get_grp_elem.length);
    let edit_chg = new Array(get_grp_elem.length);
    let edit_del = new Array(get_grp_elem.length);
    //全グループを取得する。
    for (let i = 0; i <= get_grp_elem.length-1; i++ ){
        let legend_name = get_grp_elem[i].firstElementChild.innerHTML;  //グループの名前（「グループ2 (and結合)」のような値）を持って来る。
        let grp_name = get_grp_elem[i].name;  //グループの名前（group_2 のような値）を持って来る。

        //labelエレメントの中にチェックボックスを追加する。
        //また、追加したチェックボックスの右にグループの名称を表示させる。
        let l = "group_".length;  
        edit_label[i] = document.createElement("label"); 
        edit_label[i].className = "cls_edit_elem"
        edit_label[i].innerHTML = "<br>"+legend_name.split('(')[0]; //「グループ2 (and結合)」の間の(以降を除外して設定
        //and/orの切り替えボタンを作成
        edit_chg[i] = document.createElement('input'); 
        edit_chg[i].type = 'button';
        edit_chg[i].className = 'cls_edit_elem cls_edit_button';
        edit_chg[i].name = 'edit_button_change' + grp_name.substring(l,);
        edit_chg[i].value = 'and/or 反転';
        edit_chg[i].setAttribute('onclick', 'f_group_change(document,"'+ grp_name +'")');
        //削除ボタンを作成
        edit_del[i] = document.createElement('input'); 
        edit_del[i].type = 'button';
        edit_del[i].className = 'cls_edit_elem cls_edit_button';
        edit_del[i].name = 'edit_button_delete' + grp_name.substring(l,);
        edit_del[i].value = '削除';
        edit_del[i].setAttribute('onclick', 'f_group_delete(document,"'+ grp_name +'")');
        if(i==0){edit_del[i].disabled = "disabled";}     //グループ1だけは削除禁止

        //作成したlabelタグの子要素へ、チェンジボタンと削除ボタンを追加
        edit_label[i].appendChild(edit_chg[i]);
        edit_label[i].appendChild(edit_del[i]);
        //作成したlabelタグをコントロールエリアに追加
        get_control[0].appendChild(edit_label[i]);
    }
    
    //グループモードon/offの切り替え
    //mydocument.getElementsByName("group_edit")[0].hidden = false;
}

/**グループの削除のためのリストを消す。
 */
function f_group_edit_mode_off(mydocument){
    //削除対象となったグループを確認する。
    let get_grp_elem = mydocument.getElementsByClassName("cls_edit_elem");

    //取得したエレメント（チェックボックス）を下から順に消す。
    for(let i = get_grp_elem.length - 1; i >= 0; i--){
        get_grp_elem[i].parentNode.removeChild(get_grp_elem[i]);
    }

    //グループモードon/offの切り替え
    //mydocument.getElementsByName("group_edit")[0].hidden = true;
}

/**第二引数で指定されたグループのand/orを切り換える。
 * 第二引数：対象グループ（<fieldset>）のnameを設定していることを前提とする。
 */
function f_group_change(mydocument,chg_elem){

    let get_grp_elem = mydocument.getElementsByName(chg_elem);
    let cls_nm = get_grp_elem[0].className;
    let legend_tg = get_grp_elem[0].firstChild;
    if(cls_nm.indexOf('_or',0) >= 0){
        get_grp_elem[0].className = cls_nm.replace('_or','_and');
        legend_tg.innerHTML = legend_tg.innerHTML.replace('or','and');
    }else if(cls_nm.indexOf('_and',0) >= 0){
        get_grp_elem[0].className = cls_nm.replace('_and','_or');
        legend_tg.innerHTML = legend_tg.innerHTML.replace('and','or');
    }
}

/**第二引数で指定されたグループを削除する。
 * 第二引数：対象グループ（<fieldset>）のnameを設定していることを前提とする。
 */
function f_group_delete(mydocument,del_elem){
   
    let get_grp_elem = mydocument.getElementsByName(del_elem);
    let elem_children = get_grp_elem[0].children;   //取得したグループの子要素を配列にして取得。
    let fragment = document.createDocumentFragment();   //フラグメントエリア（中間ワーク的なドキュメント）を作成

    //最後の子要素から順にフラグメントの先頭に追加。
    for(let i = elem_children.length -1 ; i >= 0 ; i--){
        if(elem_children[i].tagName=='LEGEND'){
            elem_children[i].parentNode.removeChild(elem_children[i]);
        }else{
            fragment.insertBefore(elem_children[i], fragment.firstChild);   
        }
    }
    
    //フラグメントを対象のグループ（fieldset）の前に追加する。
    get_grp_elem[0].parentNode.insertBefore(fragment,get_grp_elem[0]);
    //不要になったfieldsetを削除
    get_grp_elem[0].parentNode.removeChild(get_grp_elem[0]);

    //削除後に、グループのリストを最新化。グループモードのon/offの機能で代用。
    f_group_edit_mode_off(mydocument);
    f_group_edit_mode_on(mydocument);
}
