import requests, json, urllib3, datetime, time
import streamlit as st
import time, datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://santander.pro.dynatrace.cloudcenter.corp/e/a9b631ff-5285-454a-9b3e-4355527a91fd/api/v1"

def get_date():
  now = datetime.datetime.now()
  return now.strftime("%Y%m%d_%H%M")

def get_gc():
	global TOKEN
	request_url = url + "/v2/problems"
	headers = {"Authorization": "Api-Token " + TOKEN_1, "Accept": "application/json; charset=utf-8"}
	params = {"problemSelector":"status(\"open\")"}
	res = requests.get(request_url, headers=headers, verify=False, params=params)
	Ps = res.json()["problems"]

	for K in range(len(Ps)):
		R_numero = "NC"
		R_Proyecto = "NC"
		R_Pod = "NC"
		R_Region = "NC"
		P_service = []
		P = Ps[K]
		if P["title"] == "Long garbage-collection time" or P["title"] == "Memory resources exhausted":
			for H in range(len(P["entityTags"])):
				if P["entityTags"][H]["key"] == "PROYECTO_PaaS2.0":
					R_Proyecto = P["entityTags"][H]["value"]
					R_numero = P["displayId"]
				elif P["entityTags"][H]["key"] == "Region_test":
					R_Region = P["entityTags"][H]["value"]
				elif P["entityTags"][H]["key"] == "task":
					R_Pod = P["entityTags"][H]["value"]
			if R_Region != "NC":
				print(f'{R_numero:5} --> {R_Proyecto:40}/ {R_Pod:55} --> {R_Region}')

def tokenparameter(token=None, env=None, cluster=None,region=None,do_api=None,namespace=None,microservice=None,pod=None, delete=False, idToken=False, ldap=False):
    token = ''

    #DEV URL API
    urlapi  = "https://shuttle-openshift-heapdump-sanes-shuttlepython-dev.apps.san01bks.san.dev.bo1.paas.cloudcenter.corp"
    #PRO URL API
    #urlapi = "https://shuttle-openshift-heapdump-sanes-shuttlepython-pro.apps.san01darwin.san.pro.bo1.paas.cloudcenter.corp"

    match do_api:
        case 'namespacelist':
            request_url = f"{urlapi}/dumps/namespace_list"
            headers = {"Accept": "application/json","Authorization":'Bearer '+str(idToken),"x-clientid":"darwin"}
            body = {
                "functionalEnvironment": env,
                "cluster": cluster,
                "region": region,
                "ldap" : ldap
            }
            response = requests.post(url=request_url,headers=headers,data=json.dumps(body), verify=False,timeout=120)
            if response.status_code == 200:
                datos = response.text
                json_object = json.loads(datos)
                return json_object
            else:
                json_object = [None]
                st.write(f"No tenemos respuesta, no existe el objeto : {json_object}")
                st.write(f"El error es: {response.status_code}")

        case 'microservicelist':
            request_url = f"{urlapi}/dumps/microservices_list"
            headers = {"Accept": "application/json","Authorization":'Bearer '+str(idToken),"x-clientid":"darwin"}
            body = {
            "functionalEnvironment": env,
            "cluster": cluster,
            "region": region,
            "namespace": namespace,
            "ldap" : ldap
            }
            response = requests.post(url=request_url,headers=headers,data=json.dumps(body), verify=False,timeout=120)
            if response.status_code == 200:
                datos = response.text
                json_object = json.loads(datos)
                return json_object
            else:
                json_object = [None]
        case 'podlist':
            request_url = f"{urlapi}/dumps/pod_list"
            headers = {"Accept": "application/json","Authorization":'Bearer '+str(idToken),"x-clientid":"darwin"}
            body = {
            "functionalEnvironment": env,
            "cluster": cluster,
            "region": region,
            "namespace": namespace,
            "microservices": microservice,
            "ldap" : ldap
            }
            response = requests.post(url=request_url,headers=headers,data=json.dumps(body), verify=False,timeout=120)
            if response.status_code == 200:
                datos = response.text
                json_object = json.loads(datos)
                return json_object
            else:
                json_object = [None]

        case "heapdump":
            request_url = f"{urlapi}/dumps/heapdump"
            headers = {"Accept": "application/json","Authorization":'Bearer '+str(idToken),"x-clientid":"darwin"}
            body = {
                "functionalEnvironment": env,
                "cluster": cluster,
                "region": region,
                "namespace": namespace,
                "pod": [pod],
                "action": "1",
                "delete": delete,
                "ldap": ldap
        }
            response = requests.post(url=request_url,headers=headers,data=json.dumps(body), verify=False,timeout=200)
            if response.status_code == 200:
                return response.content
            else:
                json_object = [{"heapdump": None}]
                return json_object
            
        case "heapdump_datagrid":
            request_url = f"{urlapi}/dumps/heapdump"
            headers = {"Accept": "application/json","Authorization":'Bearer '+str(idToken),"x-clientid":"darwin"}
            body = {
                "functionalEnvironment": env,
                "cluster": cluster,
                "region": region,
                "namespace": namespace,
                "pod": [pod],
                "action": "3",
                "delete": delete,
                "ldap": ldap
        }
            response = requests.post(url=request_url,headers=headers,data=json.dumps(body), verify=False,timeout=200)
            if response.status_code == 200:
                return response.content
            else:
                json_object = [{"heapdumpdatagrid": None}]
                return json_object
            
        case "threaddump":
            request_url = f"{urlapi}/dumps/heapdump"
            headers = {"Accept": "application/json","Authorization":'Bearer '+str(idToken),"x-clientid":"darwin"}
            body = {
                "functionalEnvironment": env,
                "cluster": cluster,
                "region": region,
                "namespace": namespace,
                "pod": [pod],
                "action": "2",
                "delete": delete,
                "ldap": ldap
        }
            response = requests.post(url=request_url,headers=headers,data=json.dumps(body), verify=False,timeout=120)
            if response.status_code == 200:
                return response.content
            else:
                json_object = [{"threaddump": None}]
                return json_object
            
        case "threaddump_datagrid":
            request_url = f"{urlapi}/dumps/heapdump"
            headers = {"Accept": "application/json","Authorization":'Bearer '+str(idToken),"x-clientid":"darwin"}
            body = {
                "functionalEnvironment": env,
                "cluster": cluster,
                "region": region,
                "namespace": namespace,
                "pod": [pod],
                "action": "4",
                "delete": delete,
                "ldap": ldap
        }
            response = requests.post(url=request_url,headers=headers,data=json.dumps(body), verify=False,timeout=120)
            if response.status_code == 200:
                return response.content
            else:
                json_object = [{"threaddumpdatagrid": None}]
                return json_object

def get_jvm_dump(optionenv, optioncluster, optionregion, selectnamespace, selectpod, type, delete, idToken, ldap):
    progress_text = "⏳ Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)
    
    # Simulate the progress bar
    for percent_complete in range(100):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1, text=progress_text)  
    
    # Call the API and get the response
    response = tokenparameter(env=optionenv, cluster=optioncluster, region=optionregion, namespace=selectnamespace, pod=selectpod, do_api=type, delete=delete, idToken=idToken, ldap=ldap)
    
    # Parse the JSON response
    response_json = response.json()
    
    # Check if the response contains an error message
    if response_json.get("status") == "error":
        st.warning(f"Operation failed: {response_json.get('message')}")
    else:
        st.success('Done!')
        date = get_date()
        
        # Check if file_content is not empty and contains the expected data
        file_content = response_json.get('data')
        if file_content and file_content != [{type: None}]:
            st.download_button(
                label="Download dump file 🔽",
                data=file_content,
                file_name=f'{type}-{selectpod}-{date}.gz',
                mime='application/octet-stream',
            )
        else:
            st.warning("No data found for download.")
            
def get_jvm_dump_TEMP(optionenv, optioncluster, optionregion, selectnamespace, selectpod, type, delete, idToken, ldap):
    progress_text = "⏳ Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)
    file_content = tokenparameter(env=optionenv, cluster=optioncluster, region=optionregion, namespace=selectnamespace, pod=selectpod, do_api=type, delete=delete, idToken=idToken, ldap=ldap)
    for percent_complete in range(100):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1, text=progress_text)    
    st.success('Done!')

    date = get_date()
    if file_content != [{type: None}]:
        st.download_button(
            label="Download dump file 🔽",
            data=file_content,
            file_name=f'{type}-{selectpod}-{date}.gz',
            mime='application/octet-stream',
        )
    else:
        st.warning("No data found for download.")

def download_part(part, part_number):
    part_file_name = f'HeapDump-part-{part_number}.gz'
    st.download_button(
        label=f"Download Part {part_number}",
        data=part,
        file_name=part_file_name,
        mime='application/gzip',
    )

def recover_dumps(api_url, namespace, idToken, ldap):
    request_url = f"{api_url}/dumps/historical_dumps"
    headers = {"Accept": "application/json","Authorization":'Bearer '+str(idToken),"x-clientid":"darwin"}
    body = {"namespace": namespace,"ldap": ldap}

    response = requests.post(url=request_url,headers=headers,data=json.dumps(body), verify=False,timeout=200)

    if response:
        file_list = json.loads(response.content.decode('utf-8'))
        return file_list
    else:
        return None

def download_dump(api_url, namespace, idToken, selected_file, ldap):
    request_url = f"{api_url}/dumps/download_dump?namespace={namespace}&file_name={selected_file}&ldap={ldap}"
    headers = {"Accept": "application/octet-stream", "Authorization": 'Bearer ' + str(idToken), "x-clientid": "darwin"}

    response = requests.post(url=request_url, headers=headers, verify=False, timeout=200)

    if response.status_code == 200:
        return response.content
    else:
        return None
    
if __name__ == '__main__':
	TOKEN_1 = 'oBSioZKCTXi0-bwwtTftN'
	get_gc()