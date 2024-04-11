import source
import main
import target
from source import Source
from main import Main
from target import Target


# Testa se o tamanho do batch retornado pela função load_state corresponde ao especificado
def test_batch_size(batch_size=1000):
    source_instance = Source()  # Cria uma 'instância' da classe Source
    batch_info = source_instance.load_state(batch_size)  # Tenta carregar um batch de dados com o tamanho especificado
    if batch_info is not None:  # Verifica se algum batch foi retornado, retornando Falso caso retorne 'None'
        # Caso o tamanho (len) do batch retornado (indice 1 do tuplo retornado da funçao load_state),
        # corresponde ao tamanho especificado (caso seja retorna Verdadeiro, caso não o seja retorna Falso)
        if len(batch_info[1]) == batch_size:
            print("batch_size function test passed: Correct batch size")
            return True
        else:
            print("batch_size function test passed: Incorrect batch size")
            return False
    else:
        print("batch_size function test failed: No batch")
        return False


# Testa se a função de ordenação (merge_sort) ordena corretamente uma lista de teste em ordem ascendente e descendente.
def test_ordering_list(test_list=[3, 2, 4, 1, 5]):
    main_instance = Main(batch_size=5)  # Cria uma 'instancia' da classe 'Main' com um tamanho do batch de 5
    # Chama a função merge_sort para ordenar a lista em ordem ascendente e descendente
    sorted_list_asc = main_instance.merge_sort(a=test_list, ascending=True)
    sorted_list_desc = main_instance.merge_sort(a=test_list, ascending=False)
    # Compara as listas ordenadas com os supostos resultados esperados (usando a funçao incorporada sorted)
    if sorted_list_asc != sorted(test_list):
        print(f"The resulting list ({sorted_list_asc}) doesn't match the list sorted in ascending order")
        return False
    elif sorted_list_desc != sorted(test_list, reverse=True):
        print(f"The resulting list ({sorted_list_asc}) doesn't match the list sorted in descending order")
        return False
    # Caso coincidem as listas então retona True
    else:
        print("The ordering list test passed")
        return True


# Testa a precisão dos métodos de ordenação verificando se os valores mínimo e máximo são correspondentes
# entre dois métodos de ordenação
def test_accuracy():
    main_instance = Main(batch_size=1000)  # Cria uma instância da classe Main.
    batch_info = main_instance.source.load_state(main_instance.batch_size)  # Gera um batch de numeros
    if batch_info is not None:
        batch_data = batch_info[1]  # Caso seja gerado um batch guarda no atributo 'batch_data' o respetivo batch
        # Compara os valores mínimo e máximo entre dois métodos de ordenação
        min1, max1 = main_instance.sort(batch=batch_data, ascending=True, which=True)
        min2, max2 = main_instance.sort(batch=batch_data, ascending=False, which=False)
        if min1 != min2 or max1 != max2:
            print("The values found for the largest and smallest don't match between the two defined sorting methods")
            return False
        else:
            print("The accuracy test for the sorting methods has passed")
            return True
    print("Accuracy method test failed")
    return False


# Testa se o número total de batches processados é maior para tamanhos de batches menores, conforme é suposto
def test_batch_number():
    batch_size_small = 10
    batch_size_large = 100
    # Cria duas 'instâncias' da classe Main com tamanhos de batches diferentes
    main_instance_small = Main(batch_size=batch_size_small)
    main_instance_small.run()
    main_instance_large = Main(batch_size=batch_size_large)
    main_instance_large.run()
    # Verifica se o número de bacthes processados é, então, maior para o tamanho do batch menor.
    if main_instance_small.source.batch_nr <= main_instance_large.source.batch_nr:
        print(f"The total number of batches processed for {batch_size_small} batches isn't greater than the number of "
              f"batches for {batch_size_large}")
        return False
    # Retornado verdadeiro caso o esperado aconteça
    else:
        print("Batch number test in relation to batch size passed")
        return True


if __name__ == "__main__":
    test_batch_size()
    test_ordering_list()
    test_accuracy()
    test_batch_number()


