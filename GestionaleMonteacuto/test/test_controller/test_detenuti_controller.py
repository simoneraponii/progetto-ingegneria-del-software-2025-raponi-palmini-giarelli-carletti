import unittest
from unittest.mock import MagicMock, patch
from controller.detenuti_controller import DetenutiController
from model.detenuto.detenuto import Detenuto

class TestDetenutiController(unittest.TestCase):

    def setUp(self):
        # Patch del DAO e del RapportoController
        self.patcher_dao = patch('controller.detenuti_controller.DetenutoDAO')
        self.patcher_rapporto = patch('controller.detenuti_controller.RapportoController')
        
        self.MockDetenutoDAO = self.patcher_dao.start()
        self.MockRapportoController = self.patcher_rapporto.start()
        
        self.controller = DetenutiController()
        self.mock_dao = self.controller.detenuto_dao

    def tearDown(self):
        self.patcher_dao.stop()
        self.patcher_rapporto.stop()

    # --- Test get_detenuto ---
    def test_get_detenuto_successo(self):
        mock_detenuto = MagicMock(spec=Detenuto)
        self.mock_dao.get_by_matricola.return_value = mock_detenuto

        result = self.controller.get_detenuto("MAT123")

        self.assertEqual(result, mock_detenuto)

    def test_get_detenuto_non_trovato(self):
        self.mock_dao.get_by_matricola.return_value = None

        with self.assertRaises(Exception) as context:
            self.controller.get_detenuto("MAT123")
        
        self.assertIn("Detenuto non trovato", str(context.exception))

    def test_get_detenuto_errore_dao(self):
        self.mock_dao.get_by_matricola.side_effect = Exception("DB Error")

        with self.assertRaises(Exception) as context:
            self.controller.get_detenuto("MAT123")
        
        self.assertIn("Errore nel recupero del detenuto", str(context.exception))

    # --- Test update_detenuto ---
    def test_update_detenuto_matricola_mancante(self):
        result = self.controller.update_detenuto("", {})
        self.assertFalse(result)

    def test_update_detenuto_successo(self):
        self.mock_dao.update_detenuto.return_value = True
        
        result = self.controller.update_detenuto("MAT123", {"nome": "Mario"})
        
        self.assertTrue(result)
        self.mock_dao.update_detenuto.assert_called_with("MAT123", {"nome": "Mario"})

    def test_update_detenuto_eccezione(self):
        self.mock_dao.update_detenuto.side_effect = Exception("Errore Update")
        
        result = self.controller.update_detenuto("MAT123", {})
        
        self.assertFalse(result)

    # --- Test crea_nuovo_detenuto ---
    def test_crea_nuovo_detenuto_ubicazione_non_trovata(self):
        # Setup dati input minimi
        dati = {
            "ubicazione": {"sezione": "A", "cella": "1"},
            "datoAnagrafico": {"codiceFiscale": "CF123"},
            "pena": {"descrizione": "Furto", "dataFinePena": "2025-01-01"}
        }
        # Il DAO restituisce None per l'ubicazione
        self.mock_dao.get_id_ubicazione.return_value = None

        result = self.controller.crea_nuovo_detenuto(dati)

        self.assertFalse(result)
        self.mock_dao.create_detenuto.assert_not_called()

    def test_crea_nuovo_detenuto_anagrafica_esistente(self):
        dati = {
            "ubicazione": {"sezione": "A", "cella": "1"},
            "datoAnagrafico": {"codiceFiscale": "CF_ESISTENTE"},
            "pena": {"descrizione": "Furto", "dataFinePena": "2025"}
        }
        
        self.mock_dao.get_id_ubicazione.return_value = 1
        # Simuliamo che l'anagrafica esista già
        self.mock_dao.check_esistenza_dato_anagrafico.return_value = True

        result = self.controller.crea_nuovo_detenuto(dati)

        self.assertFalse(result)
        self.mock_dao.create_detenuto.assert_not_called()

    def test_crea_nuovo_detenuto_pena_esistente(self):
        dati = {
            "ubicazione": {"sezione": "A", "cella": "1"},
            "datoAnagrafico": {"codiceFiscale": "CF_NUOVO"},
            "pena": {"descrizione": "Furto", "dataFinePena": "2025"}
        }

        self.mock_dao.get_id_ubicazione.return_value = 1
        self.mock_dao.check_esistenza_dato_anagrafico.return_value = False
        # Simuliamo che la pena esista già
        self.mock_dao.check_esistenza_pena.return_value = True

        result = self.controller.crea_nuovo_detenuto(dati)

        self.assertFalse(result)
        self.mock_dao.create_detenuto.assert_not_called()

    def test_crea_nuovo_detenuto_successo(self):
        dati = {
            "ubicazione": {"sezione": "A", "cella": "1"},
            "datoAnagrafico": {"codiceFiscale": "CF_OK"},
            "pena": {"descrizione": "Furto", "dataFinePena": "2025"}
        }

        # Setup mock per passaggi positivi
        self.mock_dao.get_id_ubicazione.return_value = 10
        self.mock_dao.check_esistenza_dato_anagrafico.return_value = False
        self.mock_dao.check_esistenza_pena.return_value = False
        self.mock_dao.create_detenuto.return_value = True

        result = self.controller.crea_nuovo_detenuto(dati)

        self.assertTrue(result)
        self.mock_dao.create_detenuto.assert_called_with(dati)

    def test_crea_nuovo_detenuto_eccezione(self):
        dati = {"ubicazione": {"sezione": "A", "cella": "1"}}
        self.mock_dao.get_id_ubicazione.side_effect = Exception("Errore generico")

        with self.assertRaises(Exception):
            self.controller.crea_nuovo_detenuto(dati)

    # --- Test getDetenutiDto ---
    def test_get_detenuti_dto_successo(self):
        lista_dto = ["dto1", "dto2"]
        self.mock_dao.get_all_detenuti_dto.return_value = lista_dto

        result = self.controller.getDetenutiDto()

        self.assertEqual(result, lista_dto)

    def test_get_detenuti_dto_errore(self):
        self.mock_dao.get_all_detenuti_dto.side_effect = Exception("DB Fail")

        with self.assertRaises(Exception):
            self.controller.getDetenutiDto()

if __name__ == '__main__':
    unittest.main()