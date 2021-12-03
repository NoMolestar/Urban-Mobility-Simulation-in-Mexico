using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;



public class Requesting : MonoBehaviour
{
    public GameObject carrosVerticales;
    public GameObject carrosHorizontales;
    public GameObject carrosVerticales2;
    public GameObject[] semaforos;
    public List<GameObject> cars = new List<GameObject>();
    private bool flag = true;
    public float speed;

    void Start()
    {
        StartCoroutine(GetText());
    }

    IEnumerator GetText()
    {
        UnityWebRequest www = UnityWebRequest.Get("https://intersection-simulation.mybluemix.net/");
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        try
        {
            Data posiciones = JsonUtility.FromJson<Data>(www.downloadHandler.text);
            foreach (Position p in posiciones.data)
            {
                int i = 0;
                foreach (Colores pAux in p.semaforo)
                {
                    if (pAux.color == 0)
                    {
                        semaforos[i].GetComponent<Light>().color = Color.red;
                    }
                    else if (pAux.color == 1)
                    {
                        semaforos[i].GetComponent<Light>().color = Color.yellow;
                    }
                    else
                    {
                        semaforos[i].GetComponent<Light>().color = Color.green;
                    }
                    i++;
                }
                i = 0;
                foreach (Position_Aux pAux in p.posiciones)
                {
                    if (!flag)
                    {
                        if ((pAux.direccion == 2 && cars[i].transform.position.z >= 14) || (pAux.direccion == 1 && cars[i].transform.position.x <= 5) || (pAux.direccion == 0 && cars[i].transform.position.z <= 3))
                        {
                            cars[i].transform.position = new Vector3(pAux.valor[1], 0, pAux.valor[0]);
                        }
                        else
                        {
                            cars[i].transform.position = Vector3.MoveTowards(new Vector3(cars[i].transform.position.x, cars[i].transform.position.y, cars[i].transform.position.z), new Vector3(pAux.valor[1], 0, pAux.valor[0]), speed * Time.deltaTime);

                        }
                    }
                    else
                    {
                        if (pAux.direccion == 0)
                        {
                            cars.Add(Instantiate(carrosVerticales, new Vector3(pAux.valor[1], 0, pAux.valor[0]), Quaternion.identity) as GameObject);

                        }
                        else if (pAux.direccion == 1)
                        {
                            cars.Add(Instantiate(carrosHorizontales, new Vector3(pAux.valor[1], 0, pAux.valor[0]), Quaternion.identity) as GameObject);
                        }
                        else
                        {
                            cars.Add(Instantiate(carrosVerticales2, new Vector3(pAux.valor[1], 0, pAux.valor[0]), Quaternion.identity) as GameObject);
                        }
                    }
                    i += 1;
                }
                i = 0;
                flag = false;
            }
        }
        catch
        {
            Debug.Log("Colchon");
        }
        StartCoroutine(GetText());
    }
}
